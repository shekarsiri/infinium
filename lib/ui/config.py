"""
An API for interfacing with the Infinium configuration file. The only public
component is ``configuration``, an object used to access and update config file
fields. There is only one ``configuration`` object, because it is meant to be
shared between all parts of the program to keep configuration options in sync.
The ``configuration`` object is thread safe.

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
import threading
from pathlib import Path

# Third-party library imports.
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper

except ImportError:
    from yaml import Loader, Dumper

# Infinium library imports.
from lib import consts


class _Configuration:
    __FILE_NAME = '.infinium.yml'

    def __init__(self):
        self.__thread_lock = threading.Lock()
        with open(self.__FILE_NAME) as config_file:
            self.__configuration = load(config_file, Loader)

    def __update_field(self, field, new_value):
        self.__thread_lock.acquire()
        old_value = self.__configuration[field]
        self.__configuration[field] = new_value
        try:
            with open(self.__FILE_NAME, 'w') as config_file:
                dump(self.__configuration,
                     config_file,
                     Dumper=Dumper,
                     default_flow_style=False)

        except Exception:
            self.__configuration[field] = old_value
            raise

        finally:
            self.__thread_lock.release()

    @property
    def main_operation(self):
        self.__thread_lock.acquire()
        value = consts.STR_TO_MAIN_OPERATION[self.__configuration['main_operation'].lower()]
        self.__thread_lock.release()
        return value

    @main_operation.setter
    def main_operation(self, value):
        self.__update_field('main_operation', consts.MAIN_OPERATION_TO_STR[value])

    @property
    def stock_name(self):
        self.__thread_lock.acquire()
        value = self.__configuration['stock_name']
        self.__thread_lock.release()
        return value

    @stock_name.setter
    def stock_name(self, value):
        self.__update_field('stock_name', str(value))

    @property
    def database_type(self):
        self.__thread_lock.acquire()
        value = consts.STR_TO_DATABASE_TYPE[self.__configuration['database_type'].lower()]
        self.__thread_lock.release()
        return value

    @database_type.setter
    def database_type(self, value):
        self.__update_field('database_type', consts.DATABASE_TYPE_TO_STR[value])

    @property
    def database_path(self):
        self.__thread_lock.acquire()
        value = Path(self.__configuration['database_path'])
        self.__thread_lock.release()
        return value

    @database_path.setter
    def database_path(self, value):
        self.__update_field('database_path', str(value))

    @property
    def model_path(self):
        self.__thread_lock.acquire()
        value = Path(self.__configuration['model_path'])
        self.__thread_lock.release()
        return value

    @model_path.setter
    def model_path(self, value):
        self.__update_field('model_path', str(value))


configuration = _Configuration()