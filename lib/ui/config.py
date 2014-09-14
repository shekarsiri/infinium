"""
An API for interfacing with the Infinium configuration file. The only public
component is ``configuration``, an object used to access and update config file
fields. It is instantiated, and the config file read, upon import. There is
only one ``configuration`` object, because it is meant to be shared between all
parts of the program to keep configuration options in sync. The
``configuration`` object is thread safe.

The name of the configuration file is '{}'. The configuration loader first
searches for it in the current working directory, then in the location
specified by the '{}' environment variable, and finally in the root of the
Infinium installation directory, specified by the '{}' environment variable.

Upon import, this module may raise any exception that ``Path.open`` and
``yaml.load`` may raise, as well as ``ConfigFileNotFoundError``.

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

# Python standard library imports.
import threading
from pathlib import Path
from os import getenv

# Third-party library imports.
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper

except ImportError:
    from yaml import Loader, Dumper

# Infinium library imports.
from lib import consts


# Module header.
__maintainer__ = consts.Developer.JERRAD_GENSON
__contact__ = consts.Developer.EMAIL[__maintainer__]
__doc__ = __doc__.format(consts.CONFIG_FILE_NAME,
                         consts.CONFIG_VAR,
                         consts.INSTALL_VAR)


class ConfigFileNotFoundError(Exception):
    """
    Indicates the Infinium configuration file could not be found at any of the
    locations that ``_Configuration`` checks for it.
    """

    pass


class _Configuration:
    def __init__(self):
        self.__thread_lock = threading.Lock()
        cwd_config_path = Path(consts.CONFIG_FILE_NAME)
        environ_config_path = Path(getenv(consts.CONFIG_VAR,
                                          consts.DEFAULT_CONFIG_PATH)) / Path(consts.CONFIG_FILE_NAME)

        install_config_path = Path(getenv(consts.INSTALL_VAR,
                                          consts.DEFAULT_INSTALL_PATH)) / Path(consts.CONFIG_FILE_NAME)

        # First look for config file in current working directory.
        if cwd_config_path.exists():
            config_path = Path(consts.CONFIG_FILE_NAME)

        # Next, look for config file at config environment variable.
        elif environ_config_path.exists():
            config_path = environ_config_path

        # Finally try looking for config file in installation directory.
        elif install_config_path.exists():
            config_path = install_config_path

        # Config file could not be found.
        else:
            raise ConfigFileNotFoundError()

        with config_path.open() as config_file:
            self.__configuration = load(config_file, Loader)

        self.__config_path = config_path

    def __update_field(self, field, new_value):
        self.__thread_lock.acquire()
        old_value = self.__configuration[field]
        self.__configuration[field] = new_value
        try:
            with self.__config_path.open('w') as config_file:
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