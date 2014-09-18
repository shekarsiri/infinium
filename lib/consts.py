"""
Program-wide constant definitions live here.

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
from enum import Enum
from pathlib import Path


class Developer:
    """
    Defines names and email addresses of all core Infinium developers.
    """

    JERRAD_GENSON = 'Jerrad Genson'

    # Email addresses of all core Infinium developers.
    EMAIL = {JERRAD_GENSON: 'jerradgenson@neomailbox.ch'}

__maintainer__ = Developer.JERRAD_GENSON
__contact__ = Developer.EMAIL[__maintainer__]

# Name of this program.
PROGRAM_NAME = 'Infinium'


class MainOperation(Enum):
    """
    Defines end goals the user can achieve by running Infinium.
    """

    construct_model = 1
    add_database_entry = 2
    analyze_stock = 3
    exit = 4

# Maps strings to MainOperation values.
STR_TO_MAIN_OPERATION = {'construct_model': MainOperation.construct_model,
                         'add_data': MainOperation.add_database_entry,
                         'analyze_stock': MainOperation.analyze_stock}

# Maps MainOperation values to strings.
MAIN_OPERATION_TO_STR = {value: key for key, value in STR_TO_MAIN_OPERATION.items()}


class DatabaseType(Enum):
    """
    Defines supported database types.
    """

    pgsql = 1

# Maps strings to DatabaseType values.
STR_TO_DATABASE_TYPE = {'pgsql': DatabaseType.pgsql}

# Maps DatabaseType values to strings.
DATABASE_TYPE_TO_STR = {value: key for key, value in STR_TO_DATABASE_TYPE.items()}


# Name of configuration file.
CONFIG_FILE_NAME = '.infinium.yml'

# Name of config file path environment variable.
CONFIG_VAR = 'INFINIUM_CONFIG'

# Default config file location.
DEFAULT_CONFIG_PATH = Path('~/')

# Name of installation directory environment variable.
INSTALL_VAR = 'INFINIUM_INSTALL'

# Default installation location.
DEFAULT_INSTALL_PATH = Path('/usr/lib/infinium')

# Name of log file path environment variable.
LOG_VAR = 'INFINIUM_LOG'

# Default log file location.
DEFAULT_LOG_PATH = Path('.')

# Log file name.
LOG_FILE_NAME = Path('infinium.log')


class ExitCode(Enum):
    """
    Defines Infinium exit codes.
    """

    success = 0
    config_file_not_found = 1
    config_file_corrupt = 2