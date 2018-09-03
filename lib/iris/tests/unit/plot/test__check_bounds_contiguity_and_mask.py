# (C) British Crown Copyright 2018, Met Office
#
# This file is part of Iris.
#
# Iris is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Iris is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Iris.  If not, see <http://www.gnu.org/licenses/>.
"""Unit tests for the `iris.plot._check_bounds_contiguity_and_mask`
function."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# Import iris.tests first so that some things can be initialised before
# importing anything else.
import iris.tests as tests

import numpy as np
import numpy.ma as ma

from iris.coords import DimCoord
from iris.tests.stock import (sample_2d_latlons,
                              make_bounds_discontiguous_at_point)

if tests.MPL_AVAILABLE:
    import iris.plot as iplt


@tests.skip_plot
class Test_check_bounds_contiguity_and_mask(tests.IrisTest):
    def test_1d_not_checked(self):
        # Test a 1D coordinate, which is not checked as atol is not set.
        coord = DimCoord([1, 3, 5], bounds=[[0, 2], [2, 4], [5, 6]])
        data = np.array([278, 300, 282])
        iplt._check_bounds_contiguity_and_mask(coord, data)

    def test_1d_contiguous(self):
        # Test a 1D coordinate which is contiguous.
        coord = DimCoord([1, 3, 5], bounds=[[0, 2], [2, 4], [4, 6]])
        data = np.array([278, 300, 282])
        iplt._check_bounds_contiguity_and_mask(coord, data, atol=1e-3)

    def test_1d_discontigous_masked(self):
        # Test a 1D coordinate which is discontiguous but masked at
        # discontiguities.
        coord = DimCoord([1, 3, 5], bounds=[[0, 2], [2, 4], [5, 6]])
        data = ma.array(np.array([278, 300, 282]), mask=[0, 1, 0])
        iplt._check_bounds_contiguity_and_mask(coord, data, atol=1e-3)

    def test_1d_discontigous_unmasked(self):
        # Test a 1D coordinate which is discontiguous and unmasked at
        # discontiguities.
        coord = DimCoord([1, 3, 5], bounds=[[0, 2], [2, 4], [5, 6]])
        data = ma.array(np.array([278, 300, 282]), mask=[1, 0, 0])
        msg = 'coordinate are not contiguous and data is not masked where ' \
              'the discontiguity occurs'
        with self.assertRaisesRegexp(ValueError, msg):
            iplt._check_bounds_contiguity_and_mask(coord, data, atol=1e-3)

    def test_2d_contiguous(self):
        # Test a 2D coordinate which is contiguous.
        cube = sample_2d_latlons()
        iplt._check_bounds_contiguity_and_mask(cube.coord('longitude'),
                                               cube.data)

    def test_2d_discontigous_masked(self):
        # Test a 2D coordinate which is discontiguous but masked at
        # discontiguities.
        cube = sample_2d_latlons()
        make_bounds_discontiguous_at_point(cube, 3, 4)
        iplt._check_bounds_contiguity_and_mask(cube.coord('longitude'),
                                               cube.data)

    def test_2d_discontigous_unmasked(self):
        # Test a 2D coordinate which is discontiguous and unmasked at
        # discontiguities.
        cube = sample_2d_latlons()
        make_bounds_discontiguous_at_point(cube, 3, 4)
        msg = 'coordinate are not contiguous'
        cube.data[3, 4] = ma.nomask
        with self.assertRaisesRegexp(ValueError, msg):
            iplt._check_bounds_contiguity_and_mask(cube.coord('longitude'),
                                                   cube.data)


if __name__ == "__main__":
    tests.main()