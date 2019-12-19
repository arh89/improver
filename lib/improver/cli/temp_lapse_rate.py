#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# (C) British Crown Copyright 2017-2019 Met Office.
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
"""Script to calculate temperature lapse rates for given temperature and
orogrophy datasets."""

from improver import cli
from improver.constants import DALR, U_DALR


@cli.clizefy
@cli.with_output
def process(temperature: cli.inputcube,
            orography: cli.inputcube = None,
            land_sea_mask: cli.inputcube = None,
            *,
            max_height_diff_metres: float = 35,
            nbhood_radius: int = 7,
            max_lapse_rate: float = -3*DALR,
            min_lapse_rate: float = DALR,
            return_dalr=False):
    """Calculate temperature lapse rates in units of K m-1 over orography grid.

    Args:
        temperature (iris.cube.Cube):
            Air temperature data. This is required even when returning DALR,
            as this defines the grid on which lapse rates are required.
        orography (iris.cube.Cube):
            Orography data.
        land_sea_mask (iris.cube.Cube):
            Binary land-sea mask data. True for land-points, False for sea.
        max_height_diff_metres (float):
            Maximum allowable height difference between the central point and
            points in the neighbourhood over which the lapse rate will be
            calculated.
        nbhood_radius (int):
            Radius of neighbourhood in grid points around each point. The
            neighbourhood is a square array with side length
            2*nbhood_radius + 1. The default value of 7 is from the reference
            paper (see plugin documentation).
        max_lapse_rate (float):
            Maximum lapse rate allowed, in K m-1.
        min_lapse_rate (float):
            Minimum lapse rate allowed, in K m-1.
        return_dalr (bool):
            If True, returns a cube containing the dry adiabatic lapse rate
            rather than calculating the true lapse rate.

    Returns:
        iris.cube.Cube:
            Lapse rate (K m-1)

    Raises:
        ValueError: If minimum lapse rate is greater than maximum.
        ValueError: If Maximum height difference is less than zero.
        ValueError: If neighbourhood radius is less than zero.

    """
    import numpy as np
    from improver.lapse_rate import LapseRate
    from improver.metadata.amend import amend_attributes

    attributes_dict = {"title": "remove", "source": "remove",
                       "history": "remove", "um_version": "remove"}

    if return_dalr:
        result = temperature.copy(
            data=np.full_like(temperature.data, U_DALR.points[0]))
        result.rename('air_temperature_lapse_rate')
        result.units = U_DALR.units
        amend_attributes(result, attributes_dict)
        return result

    if min_lapse_rate > max_lapse_rate:
        msg = 'Minimum lapse rate specified is greater than the maximum.'
        raise ValueError(msg)

    if max_height_diff_metres < 0:
        msg = 'Maximum height difference specified is less than zero.'
        raise ValueError(msg)

    if nbhood_radius < 0:
        msg = 'Neighbourhood radius specified is less than zero.'
        raise ValueError(msg)

    result = LapseRate(
        max_height_diff=max_height_diff_metres,
        nbhood_radius=nbhood_radius,
        max_lapse_rate=max_lapse_rate,
        min_lapse_rate=min_lapse_rate).process(
            temperature, orography, land_sea_mask)
    amend_attributes(result, attributes_dict)
    return result
