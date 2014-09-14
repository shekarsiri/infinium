"""
An API for interfacing with the Infinium configuration file. The only public
component is ``configuration``, an object used to access and mutate config file
fields. There is only one ``configuration`` object, because it is meant to be
shared between all parts of the program to keep configuration options in sync.
Not currently thread or process safe.

Upon import, this module may raise any exception that ``open`` and ``yaml.load``
may raise.

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
from pathlib import Path

# Third-party library imports.
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper

except ImportError:
    from yaml import Loader, Dumper

# Infinium library imports.
from lib.ui.base import EndGoal, DatabaseType


class _Configuration:
    __FILE_NAME = '.infinium.yml'
    __END_GOAL_MAP = {'construct model': EndGoal.construct_model,
                      'add database entry': EndGoal.add_database_entry,
                      'analyze stock': EndGoal.analyze_stock}

    __DATABASE_TYPE_MAP = {'yml': DatabaseType.yml}

    def __init__(self):
        with open(self.__FILE_NAME) as config_file:
            self.__configuration = load(config_file, Loader)

    @property
    def end_goal(self):
        return self.__END_GOAL_MAP[self.__configuration['end_goal'].lower()]

    @property
    def stock_key(self):
        return self.__configuration['stock_key']

    @property
    def database_type(self):
        return self.__DATABASE_TYPE_MAP[self.__configuration['database_type'].lower()]

    @property
    def database_path(self):
        return Path(self.__configuration['database_path'])

    @property
    def model_path(self):
        return Path(self.__configuration['model_path'])


configuration = _Configuration()