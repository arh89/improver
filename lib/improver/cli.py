# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# (C) British Crown Copyright 2017-2018 Met Office.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""IMPROVER CLI base class."""

import sys
from sets import Set
import inspect

from improver.argparser import ArgParser
from improver.utilities.load import load_cube  # as DEFAULT_LOADER
from improver.utilities.save import save_netcdf  # as DEFAULT_SAVER


DEFAULT_LOADER = load_cube
DEFAULT_SAVER = save_netcdf

# argument_mapping looks like:
# {'cli_argument': '__init__.argument'} etc..
# {'input_filepath': 'LOADER.cube'}
class CLI(object):

    # TODO: this might be the order that the methods are called...?
    SUPPORTED_PLUGIN_METHODS = ('__init__', 'process')

    SPECIAL_FUNCTIONS = ('LOADER', 'SAVER')

    def __init__(self, plugin, argument_mapping, cli_argspecs=None,
                 description=None, loader=DEFAULT_LOADER, saver=DEFAULT_SAVER):
        """Create a CLI for a plugin.
        The ArgParser instance is created automatically."""

        self.plugin = plugin
        self.loader = loader
        self.saver = saver

        # We assume that all plugins are currently implemented as classes
        # with __init__ and process methods.
        # To enforce: check that the plugin has only methods which are
        # contained within CLI.SUPPORTED_PLUGIN_METHODS - this will not be
        # necessary once all plugins inherit from a common base class
        self._check_plugin_conforms()

        # for user friendliness, we choose the input argument_mapping to look
        # like: { 'cli_argument': 'plugin_method.method_argument' }
        # but processing is easier if our dictionary looks like:
        # { 'plugin_method': { 'method_argument': 'cli_argument' } }
        # ...let's restructure:
        cli_method_args = self._reorder_mapping_dict(argument_mapping)

        # There are some special functions which are treated differently
        special_args = {}
        for special_function in CLI.SPECIAL_FUNCTIONS:
            # special_function will always be a key (reorder_mapping_dict will
            # add it if necessary)
            special_args[special_function] = cli_method_args[special_function]
            del cli_method_args[special_function]

        # argument_mapping contains the mapping from cli arguments to
        # plugin method arguments - we need to check two things:
        # 1. that the methods are plugin methods that we know how to handle
        #    (i.e: that they are in CLI.SUPPORTED_PLUGIN_METHODS)
        self._check_cli_methods_supported(cli_method_args.keys())

        # 2. that the provided arguments to these methods are actually
        #    arguments to these methods.

        # first get the actual plugin method args (and defaults)
        actual_plugin_method_args, actual_plugin_method_defaults = (
            self._get_plugin_method_args_and_defaults())

#        # we want to check that there is a 'cube' on in the arguments of the
#        # plugin's process method, and that it has no default - this will not
#        # be passed in directly from the command line, but is mapped to the
#        # loader's output (which requires an input filepath)
#        cube_not_in_process = ('cube' not in
#                               actual_plugin_method_args['process'])
#        cube_has_default = ('cube' in actual_plugin_method_defaults['process'])
#        if cube_not_in_process or cube_has_default:
#            raise AttributeError("`cube` must exist in the plugin's `process` "
#                                 "method's argument list and must not have "
#                                 "a default value.")

        # do the desired method args agree?
        for plugin_method in CLI.SUPPORTED_PLUGIN_METHODS:
            plugin_method_args = actual_plugin_method_args[plugin_method]
            desired_cli_method_args = cli_method_args[plugin_method].keys()
            if not Set(desired_cli_method_args).issubset(
                Set(plugin_method_args)):
                # give more detail here... and raise better exception
                raise Exception("Method argument(s) provided in the argument "
                                "mapping did not exist on the plugin's "
                                "methods.")

        # LOADER will create cubes, so we need to ensure that the cubes created
        # by loader can pass through to the process method..
        # note, these ONLY go to the process method..
        loader_cubes = special_args['LOADER'].keys()

        # what if there are plugin method args which are not provided in the
        # CLI argument mapping?
        # it's okay if these have defaults - should we check?
        # should fall over if they don't have defaults when being called anyway
        for plugin_method in CLI.SUPPORTED_PLUGIN_METHODS:
            plugin_method_args = actual_plugin_method_args[plugin_method]
            desired_cli_method_args = cli_method_args[plugin_method].keys()
            # add LOADER created cubes here:...
            if plugin_method == 'process':
                desired_cli_method_args += loader_cubes
            # desired_cli_methods_args should be a subset of plugin_method_args
            unmapped_plugin_method_args = list(Set(plugin_method_args) -
                                            Set(desired_cli_method_args))
            if len(unmapped_plugin_method_args) > 0:
                for arg in unmapped_plugin_method_args:
                    if arg not in actual_plugin_method_defaults[plugin_method]:
                        raise Exception("Not all plugin methods arguments "
                                        "were fully specified. Either pass in "
                                        "from the CLI, or set a default.")
        # now get the mapping?
        # certain arguments, e.g: `cube` on the process method, will be created
        # from the loader and input filepath

        # want some information about the options...
        plugin_argspecs_dict = {}
        for plugin_method in CLI.SUPPORTED_PLUGIN_METHODS:
            method_argspecs = self._derive_argparser_argspecs(
                                actual_plugin_method_args[plugin_method],
                                actual_plugin_method_defaults[plugin_method])
            plugin_argspecs_dict[plugin_method] = method_argspecs

        # we do not get the method args and defaults for LOADER and SAVER,
        # it is assumed that the loader takes a single filepath, and the saver
        # takes a cube and a filepath...
        for special_function, cube_arg_mapping in special_args.items():
            argspecs_dict[special_function] = []
            for cube_name, cli_arg in cube_arg_mapping:
                argspecs_dict[special_function].append([]

        print argspecs_dict

#        # TODO: Need to think about what happens if both have the same flag
#        # name, because it is wrapped in a list...
#        plugin_specific_argspecs = init_argspecs + process_argspecs
#
#        plugin_description = inspect.getdoc(self.plugin)
#
#        cli_args = ArgParser(central_arguments=('input_file', 'output_file'),
#                             specific_arguments=plugin_specific_argspecs,
#                             **{'description': plugin_description}
#                            ).parse_args()
#
#        cli_args = vars(cli_args)
#        self.args = {}
#        for method_name, method_arg_cli_mapping in cli_method_args.items():
#            self.args[method_name] = {}
#            for method_arg, cli_arg in method_arg_cli_mapping:
#                self.args[method_name][method_arg] = cli_args[cli_arg]

#        self.input_file = cli_args.input_filepath
#        self.output_file = cli_args.output_filepath
#
        # map what was passed in from the command line, to the actual
        # method arguments


    def _check_plugin_conforms(self):
        """Check that the plugin has the methods which are required for the CLI
        to function.
        """
        # eventually once all plugins inherit from a BasePlugin class, we can
        # guarantee that they have these methods - for now, manually check
        for method_name in CLI.SUPPORTED_PLUGIN_METHODS:
            method = getattr(self.plugin, method_name, None)
            if method is None or not callable(method):
                raise AttributeError("Plugin class does not conform to "
                                     "specification.")

    @staticmethod
    def _check_cli_methods_supported(cli_method_names):
        """Check that the plugin methods which were passed in from the argument
        mapping are a subset of the plugin methods that this class knows how to
        deal with.
        ie: There must be no methods passed in from the argument mapping that
        the CLI doesn't understand.

        There can be methods on the plugin that the CLI knows how to handle,
        but that were not passed in from the argument mapping - in this case,
        they *must* have defaults in the plugin, or it will fail to work.
        """
        # TODO: Do we check the last statement of the docstring somewhere?
        if not Set(cli_method_names).issubset(
            Set(CLI.SUPPORTED_PLUGIN_METHODS)):
            # choose more appropriate exception
            raise Exception("Unsupported plugin method included in the CLI "
                            "argument mapping.")

    def _get_plugin_method_args_and_defaults(self):
        """Given a plugin, work out all of the arguments and defaults for each
        of the methods (that are supported).
        Returns: Two dictionaries: both keyed by the method name,
        one for the arguments (values are: a list),
        one for the defaults (values are dictionaries, keys being the argument
        names, values being the default values.

        If an argument does not have a default, it will not be a key in the
        (method) defaults dictionary.
        """
        # TODO: explain what happens if an argument doesn't have a default
        method_arg_mapping_dict = {}
        method_default_mapping_dict = {}
        for method_name in CLI.SUPPORTED_PLUGIN_METHODS:
            method = getattr(self.plugin, method_name)
            method_args, method_defaults = self._method_args_and_defaults(
                                            method)
            method_arg_mapping_dict[method_name] = method_args
            method_default_mapping_dict[method_name] = method_defaults
        return method_arg_mapping_dict, method_default_mapping_dict

    @staticmethod
    def _method_args_and_defaults(method):
        """For a particular method, return a list of its arguments (excluding
        self) and a dictionary containing the defaults (if any) - keyed by the
        argument name (if an argument has no default, it will not be in the
        dictionary).
        """
        # we do not support varargs or kwargs as it would be difficult to
        # automatically construct a CLI from these...
        argspec = inspect.getargspec(method)
        args = argspec.args
        defaults = argspec.defaults if argspec.defaults is not None else []

        # for instance methods, self will always be the first argument
        # (but remove from anywhere in list...):
        args = [arg for arg in args if arg != 'self']

        # now setup defaults if they exist:
        # (removal of self will not affect results, since self will not have a
        # default)
        args_defaults = {}
        for arg, default in zip(args[-len(defaults):], defaults):
            args_defaults[arg] = default
        return args, args_defaults

    @staticmethod
    def _reorder_mapping_dict(argument_mapping):
        """For user friendliness: the argument_mapping looks like:
        {'cli_argument': 'plugin_method.argument'} etc..

        But for programmer friendliness, it is better if the dictionary is
        restructured: the keys should be the plugin method names, where the
        values are dictionaries which have the plugin method arguments as their
        keys, and strings representing the cli argument as the values.
        """
        # This is the mapping we want to enforce:
        list_of_keys = (list(CLI.SUPPORTED_PLUGIN_METHODS) +
                        list(CLI.SPECIAL_FUNCTIONS))

        # initialize to dict where values are empty dictionaries:
        method_arg_mapping_dict = dict(map(lambda method: (method, {}),
                                       list_of_keys))

        for cli_arg, method_arg in argument_mapping.items():
            method, arg = method_arg.split('.')
            # reorder dict?
            method_arg_mapping_dict[method][arg] = cli_arg
        return method_arg_mapping_dict

    @staticmethod
    def _derive_argparser_argspecs(arglist, argdefaults):
        """Given a list of arguments and a dictionary containing defaults
        (where the keys are a subset of the arglist), create a list of argspecs
        which can be used to create an ArgParser instance.
        """
        # argdefaults is a dictionary, arglist is a list of strings
        argspecs = []
        for argname in arglist:
            argdefault = argdefaults.get(argname, None)
            if argdefault is not None:
                # can do some fancy stuff here...
                argflags = ['--' + argname]
                argkwargs = {}
                if type(argdefault) is bool:
                    argkwargs['action'] = 'store_true'
                argkwargs['default'] = argdefault
            else:
                argflags = [argname]
                argkwargs = {}
            argspecs.append((argflags, argkwargs))
        return argspecs

    def execute(self):
        cube = self.loader(self.input_file)
        plugin_instance = self.plugin(**self.args['__init__'])
        cube = plugin_instance.process(cube=cube,
                                       **self.args['process'])
        self.saver(cube, self.output_file)
        return cube

def main():
#   print inspect.getdoc(SomePlugin.process)
    class SomePlugin(object):

        def __init__(self, test):
            pass

        def process(self, cube):
            pass

    improver_cli = CLI(SomePlugin, {'--test': '__init__.test', 'input': 'LOADER.cube'})
    #cube = improver_cli.execute()

if __name__ == '__main__':
    main()
