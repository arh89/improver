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

import iris
from dask.distributed import Client, LocalCluster
from improver.utilities.cube_manipulation import concatenate_cubes

class ParallelProcessing(object):
    def __init__(self, plugin, slices_over, nprocs=1):
        cluster = LocalCluster(n_workers=nprocs,
                               processes=True)
#                               diagnostics_port=None)
        self.client = Client(cluster)
        self.plugin = plugin
        self.slices_over = slices_over

    def merge(self, cubes):
        if isinstance(cubes, iris.cube.Cube):
            return cubes
        if len(cubes) > 1:
            combined_cube = concatenate_cubes(cubes,
                coords_to_slice_over=self.slices_over)
        else:
            combined_cube = cubes[0]
        return combined_cube

    def process(self, cube):
        cube_slices = cube.slices_over(self.slices_over)
        futures = self.client.scatter(cube_slices)
        futures = self.client.map(self.plugin.process, futures)
        results = self.client.gather(futures)
        self.client.close()
        return self.merge(list(results))
