"""
An API for interfacing with the Infinium configuration file. The only public
component is ``get_config``, which returns a ``configuration`` object used to
access and update config file fields. There is only one ``configuration``
object, because it is meant to be shared between all parts of the program to
keep configuration options in sync.

The name of the configuration file is '{}'. The configuration loader first
searches for it in the current working directory, then in the location
specified by the '{}' environment variable, and finally in the root of the
Infinium installation directory, extracted from argv[0].

This module is thread safe.

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
from lib import data


# Module header.
__maintainer__ = data.Developer.JERRAD_GENSON
__contact__ = data.Developer.EMAIL[__maintainer__]
__doc__ = __doc__.format(data.CONFIG_FILE_NAME,
                         data.CONFIG_VAR,
                         data.INSTALL_PATH)


# Global module variables used to keep configuration file in sync.
_configuration = None
_thread_lock = threading.Lock()


def get_config():
    """
    Get Infinium configuration object.

    Returns
      The configuration object.

    Raises
      Any exception that ``Path.open`` and ``yaml.load`` may raise, as well as
      ``ConfigFileNotFoundError``.

    """

    global _configuration

    _thread_lock.acquire()
    if not _configuration:
        _configuration = _Configuration()

    _thread_lock.release()
    return _configuration


class ConfigurationError(Exception):
    """
    Indicates a general error with the configuration object. Base Exception
    for  ``config``. All other exceptions should inherit from this.
    """

    pass


class ConfigFileNotFoundError(ConfigurationError):
    """
    Indicates the Infinium configuration file could not be found at any of the
    locations that ``_Configuration`` checks for it.
    """

    pass


class ConfigFileCorruptError(ConfigurationError):
    """
    Indicates the configuration file has become corrupted.
    Example: name of a field was inadvertently changed.
    """

    pass


class _Configuration:
    def __init__(self):
        cwd_config_path = Path(data.CONFIG_FILE_NAME)
        environ_config_path = Path(getenv(data.CONFIG_VAR,
                                          data.DEFAULT_CONFIG_PATH)) / data.CONFIG_FILE_NAME

        install_config_path = data.INSTALL_PATH / data.CONFIG_FILE_NAME

        # First look for config file in current working directory.
        if cwd_config_path.exists():
            config_path = Path(data.CONFIG_FILE_NAME)

        # Next, look for config file at config environment variable.
        elif environ_config_path.exists():
            config_path = environ_config_path

        # Finally try looking for config file in installation directory.
        elif install_config_path.exists():
            config_path = install_config_path

        # Config file could not be found.
        else:
            msg = 'The configuration file could not be found.'
            raise ConfigFileNotFoundError(msg)

        with config_path.open() as config_file:
            self.__configuration = load(config_file, Loader)

        self.__config_path = config_path

    def __update_field(self, field, new_value):
        _thread_lock.acquire()
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
            _thread_lock.release()

    def __handle_key_error(self, field_name):
        msg = 'Config file field "{}" missing from config file "{}".'
        msg = msg.format(field_name, self.config_path)
        raise ConfigFileCorruptError(msg)

    @property
    def config_path(self):
        return self.__config_path

    @property
    def main_operation(self):
        _thread_lock.acquire()
        try:
            value = data.STR_TO_MAIN_OPERATION[self.__configuration['main_operation'].lower()]

        except KeyError:
            self.__handle_key_error('main_operation')

        finally:
            _thread_lock.release()

        return value

    @main_operation.setter
    def main_operation(self, value):
        self.__update_field('main_operation', data.MAIN_OPERATION_TO_STR[value])

    @property
    def stock_name(self):
        _thread_lock.acquire()
        try:
            value = self.__configuration['stock_name']

        except KeyError:
            self.__handle_key_error('stock_name')

        finally:
            _thread_lock.release()

        return value

    @stock_name.setter
    def stock_name(self, value):
        self.__update_field('stock_name', str(value))

    @property
    def database_type(self):
        _thread_lock.acquire()
        try:
            value = data.STR_TO_DATABASE_TYPE[self.__configuration['database_type'].lower()]

        except KeyError:
            self.__handle_key_error('database_type')

        finally:
            _thread_lock.release()

        return value

    @database_type.setter
    def database_type(self, value):
        self.__update_field('database_type', data.DATABASE_TYPE_TO_STR[value])

    @property
    def database_path(self):
        _thread_lock.acquire()
        try:
            value = Path(self.__configuration['database_path'])

        except KeyError:
            self.__handle_key_error('database_path')

        finally:
            _thread_lock.release()

        return value

    @database_path.setter
    def database_path(self, value):
        self.__update_field('database_path', str(value))

    @property
    def model_path(self):
        _thread_lock.acquire()
        try:
            value = Path(self.__configuration['model_path'])

        except KeyError:
            self.__handle_key_error('model_path')

        finally:
            _thread_lock.release()

        return value

    @model_path.setter
    def model_path(self, value):
        self.__update_field('model_path', str(value))