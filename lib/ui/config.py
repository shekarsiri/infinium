"""
Functions for interfacing with the Infinium configuration file.

Copyright 2014 Jerrad M. Genson

This file is part of Infinium.

Infinium is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Infinium is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Infinium.  If not, see <http://www.gnu.org/licenses/>.

"""

__author__ = 'Jerrad Genson'
__contact__ = 'jerradgenson@neomailbox.ch'


# Python standard library imports.
from enum import Enum

# Third-party library imports.
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper

except ImportError:
    from yaml import Loader, Dumper


class _Configuration:
    def __init__(self):
        pass

    @property
    def end_goal(self):
        pass

    @property
    def database_type(self):
        pass

    @property
    def database_location(self):
        pass

    @property
    def model_path(self):
        pass


configuration = _Configuration()