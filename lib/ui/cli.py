"""
Implements a command line interface for Infinium.

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

# Infinium library imports.
from lib.ui import base
from lib.ui.config import configuration


class CommandLineInterface(base.UserInterface):
    """
    User interface for running Infinium from the command line using command
    line arguments and a configuration file.

    Args
      cl_args: command line arguments from ``infinium.parse_command_line``.

    """

    def __init__(self, cl_args):
        self.__cl_args = cl_args

    @property
    def main_operation(self):
        return self.__cl_args.main_operation or configuration.main_operation

    @property
    def model_path(self):
        return self.__cl_args.model_path or configuration.model_path

    def show_test_results(self):
        raise NotImplementedError('`show_test_results` not yet implemented!')