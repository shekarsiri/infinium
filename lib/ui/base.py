"""
Contains abstract base class from which all user interfaces should inherit, as
well as other generic functions and data.

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
from abc import ABCMeta, abstractproperty, abstractmethod


class MainOperation(Enum):
    """
    Defines end goals the user can achieve by running Infinium.
    """

    construct_model = 1
    add_database_entry = 2
    analyze_stock = 3
    exit = 4


class DatabaseType(Enum):
    """
    Defines supported database types.
    """

    yml = 1


class UserInterface(metaclass=ABCMeta):
    """
    Abstract base class that all user interfaces should inherit from.
    Subclasses that override ``__init__`` should have the same parameter list
    as ``UserInterface.__init__`` or accept ``*args`` and ``**kwargs``.

    Args
      cl_args: command line arguments from ``infinium.parse_command_line``.
    """

    @abstractproperty
    def main_operation(self):
        """
        The end goal of this iteration of the main event loop.
        Must be a value defined by ``MainOperation``.
        """

        pass

    @abstractproperty
    def database_type(self):
        """
        The type of database to connect with.
        Must be a value defined by DatabaseType.
        """

        pass

    @abstractproperty
    def database_path(self):
        """
        The location of the database to connect with as a Path object.
        """

        pass

    @abstractproperty
    def model_path(self):
        """
        Path to the valuation model file. Must be a ``Path`` object.
        """

        pass

    @abstractmethod
    def show_test_results(self, test_results):
        """
        Show results from testing the valuation model to the user.

        Args
          test_results: ???

        Returns
          None

        """

        pass