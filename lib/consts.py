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

__author__ = 'Jerrad Genson'
__contact__ = 'jerradgenson@neomailbox.ch'

# Python standard library imports.
from enum import Enum

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

    yml = 1

# Maps strings to DatabaseType values.
STR_TO_DATABASE_TYPE = {'yml': DatabaseType.yml}

# Maps DatabaseType values to strings.
DATABASE_TYPE_TO_STR = {value: key for key, value in STR_TO_DATABASE_TYPE.items()}