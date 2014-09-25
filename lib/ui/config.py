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
        environ_config_dir = Path(getenv(data.CONFIG_VAR, data.DEFAULT_CONFIG_PATH))
        environ_config_path = environ_config_dir / data.CONFIG_FILE_NAME
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

    def __update_field(self, section, field, new_value):
        new_value = str(new_value)
        _thread_lock.acquire()
        old_value = self.__configuration[section][field]
        self.__configuration[section][field] = new_value
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

    def __get_field(self, section, field):
        field = str(field)
        _thread_lock.acquire()
        try:
           return self.__configuration[section][field]

        except KeyError:
            self.__handle_key_error(section, field)

        finally:
            _thread_lock.release()

    def __handle_key_error(self, section, field_name):
        msg = 'Config file section "{}" field "{}" missing from config file "{}".'
        msg = msg.format(section, field_name, self.config_path)
        raise ConfigFileCorruptError(msg)


    ## general section ##
    @property
    def config_path(self):
        return self.__config_path

    @property
    def model_path(self):
        return self.__get_field('general', 'model_path')

    @model_path.setter
    def model_path(self, value):
        self.__update_field('general', 'model_path', value)

    @property
    def log_path(self):
        return self.__get_field('general', 'log_path')

    @log_path.setter
    def log_path(self, value):
        self.__update_field('general', 'log_path', value)


    ## sgd_classifier section ##
    @property
    def sgd_loss(self):
        return self.__get_field('sgd_classifier', 'loss')

    @property
    def sgd_penalty(self):
        return self.__get_field('sgd_classifier', 'penalty')

    @property
    def sgd_alpha(self):
        return float(self.__get_field('sgd_classifier', 'alpha'))

    @property
    def sgd_l1_ratio(self):
        return float(self.__get_field('sgd_classifier', 'l1_ratio'))

    @property
    def sgd_fit_intercept(self):
        return bool(self.__get_field('sgd_classifier', 'fit_intercept'))

    @property
    def sgd_n_iter(self):
        return int(self.__get_field('sgd_classifier', 'n_iter'))

    @property
    def sgd_shuffle(self):
        return bool(self.__get_field('sgd_classifier', 'shuffle'))

    @property
    def sgd_verbose(self):
        return bool(self.__get_field('sgd_classifier', 'verbose'))

    @property
    def sgd_n_jobs(self):
        return int(self.__get_field('sgd_classifier', 'n_jobs'))

    @property
    def sgd_learning_rate(self):
        return self.__get_field('sgd_classifier', 'learning_rate')

    @property
    def sgd_eta0(self):
        return float(self.__get_field('sgd_classifier', 'eta0'))

    @property
    def sgd_power_t(self):
        return float(self.__get_field('sgd_classifier', 'power_t'))


    ## database section ##
    @property
    def db_dialect(self):
        return self.__get_field('database', 'dialect')

    @property
    def db_driver(self):
        return self.__get_field('database', 'driver')

    @property
    def db_username(self):
        return self.__get_field('database', 'username')

    @property
    def db_password(self):
        return self.__get_field('database', 'password')

    @property
    def db_host(self):
        return self.__get_field('database', 'host')

    @property
    def db_port(self):
        return self.__get_field('database', 'port')

    @property
    def db_database(self):
        return self.__get_field('database', 'database')

    @property
    def db_echo(self):
        return bool(self.__get_field('database', 'echo'))