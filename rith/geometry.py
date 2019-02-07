"""Arithmetic Geometry Extension for geoalchemy2.

Created by Joshua Powell on 02/02/2019.

Copyright (c) 2019 Joshua Powell, L.L.C. All rights reserved.

For license and copyright information please see the LICENSE.md (the "License")
document packaged with this software. This file and all other files included in
this packaged software may not be used in any manner except in compliance with
the License. Software distributed under this License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTY, OR CONDITIONS OF ANY KIND, either express or
implied.

See the License for the specific language governing permission and limitations
under the License.
"""


from geoalchemy2 import Geometry
from geoalchemy2.functions import GenericFunction


class ST_GeomFromGeoJSON(GenericFunction):
    """Add ST_GeomFromGeoJSON capabilities to geoalchemy2."""

    name = 'ST_GeomFromGeoJSON'
    type = Geometry
