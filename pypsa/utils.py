
## Copyright 2015-2019 Tom Brown (FIAS), Jonas Hoersch (FIAS), Fabian Neumann (KIT)

## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 3 of the
## License, or (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""General utility functions.
"""

# make the code as Python 3 compatible as possible
from __future__ import division
from __future__ import absolute_import
from six import iteritems, string_types


__author__ = "Tom Brown (FIAS), Jonas Hoersch (FIAS), Fabian Neumann (KIT)"
__copyright__ = "Copyright 2015-2019 Tom Brown (FIAS), Jonas Hoersch (FIAS), Fabian Neumann (KIT), GNU GPL 3"


import numpy as np

def _normed(s):
    tot = s.sum()
    if tot == 0:
        return 1.
    else:
        return s/tot

def _flatten_multiindex(m, join=' '):
    if m.nlevels <= 1: return m
    levels = map(m.get_level_values, range(m.nlevels))
    return reduce(lambda x, y: x+join+y, levels, next(levels))

def _make_consense(component, attr):
    def consense(x):
        v = x.iat[0]
        assert ((x == v).all() or x.isnull().all()), (
            "In {} cluster {} the values of attribute {} do not agree:\n{}"
            .format(component, x.name, attr, x)
        )
        return v
    return consense

def _haversine(coords):
    lon, lat = np.deg2rad(np.asarray(coords)).T
    a = np.sin((lat[1]-lat[0])/2.)**2 + np.cos(lat[0]) * np.cos(lat[1]) * np.sin((lon[0] - lon[1])/2.)**2
    return 6371.000 * 2 * np.arctan2( np.sqrt(a), np.sqrt(1-a) )

def ind_select(c, sel=None):
    """
    Returns intersection of c.ind and indices of operative lines for passive branch components.
    
    Parameters
    ==========
    sel : string
        Specifies selection of passive branches. If None it includes both operative and
        inoperative lines. If 'operative' it includes only operative lines.
        If 'inoperative' it includes only inoperative lines.
    
    Returns
    =======
    pandas.Index
    """

    if c.name=='Line' and sel is not None:

        if sel=='operative':
            selection_b = c.df.operative == True
        elif sel=='inoperative':
            selection_b = c.df.operative == False

        selection_i = c.df[selection_b].index

        if c.ind is None:
            s = selection_i
        else:
            s = c.ind.intersection(selection_i)

    else:

        if c.ind is None:
            s = slice(None)
        else:
            s = c.ind

    return s