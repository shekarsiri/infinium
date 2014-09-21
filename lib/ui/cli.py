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

# Python standard library imports.
import sys
from enum import Enum

# Infinium library imports.
import argparse
from lib.ml import construct_model
from lib.data import PROGRAM_NAME, Developer, ExitCode


__maintainer__ = Developer.JERRAD_GENSON
__contact__ = Developer.EMAIL[__maintainer__]


WELCOME_MESSAGE = """
Welcome to Infinium - bleeding-edge stock valuation software.

Copyright 2014 Jerrad M. Genson

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


def launch_cli(configuration):
    """
    Launch command line interface event loop.

    Args
      cl_args: Command line arguments from ``parse_command_line``.
      configuration: Configuration object from ``config.get_config``.

    Return
      None; does not return. Terminates program upon completion.

    """

    user_interface = CommandLineInterface()
    user_interface.show_welcome()

    # Enter CLI event loop.
    while True:
        # Decide whether to analyze a stock, add a new entry to the database,
        # or construct a new valuation model.
        user_interface.main_prompt()
        if user_interface.main_operation is MainOperation.construct_model:
            construct_model(configuration)

        elif user_interface.main_operation is MainOperation.add_database_entry:
            raise NotImplementedError('`add_database_entry` operation not yet implemented.')

        elif user_interface.main_operation is MainOperation.analyze_stock:
            raise NotImplementedError('`analyze_stock` operation not yet implemented.')

        elif user_interface.main_operation is MainOperation.exit:
            sys.exit(ExitCode.success)


def parse_command_line():
    """
    Parse command line arguments to Infinium.

    Return
      An instance of ``argparse.Namespace``.

    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        help='Launch {} in verbose mode. Redirect logging to stdout.'.format(PROGRAM_NAME),
                        action='store_true',
                        dest='verbose')

    parser.add_argument('-d', '--debug',
                        help='Launch {} in debug mode. Log debug information.'.format(PROGRAM_NAME),
                        action='store_true',
                        dest='debug')

# TODO: Uncomment when GUI is ready to be used.
#    parser.add_argument('-g', '--graphical',
#                        help='Launch {} with GUI. Note: currently not functional.'.format(PROGRAM_NAME),
#                        action='store_true',
#                        dest='graphical')

    cl_args = parser.parse_args()

    # TODO: Remove when GUI is ready to be used
    setattr(cl_args, 'graphical', False)

    return cl_args


class CommandLineInterface:
    """
    User interface for running Infinium from the command line.
    """

    def __init__(self):
        self.__main_operation = None

    @property
    def main_operation(self):
        """ User selection from `main_prompt`. """

        return self.__main_operation

    def show_welcome(self):
        """ Display Infinium welcome message. """

        print(WELCOME_MESSAGE)

    def main_prompt(self):
        """ Prompt user to select main operation. """

        while True:
            print('Choose one of the following numeric options:')
            print('  1 - Construct model')
            print('  2 - Add database entry')
            print('  3 - Analyze stock')
            print('  4 - Exit')
            selection = input('\nEnter selection: ')
            try:
                self.__main_operation = MainOperation(int(selection))
                return

            except ValueError:
                print('\nYou must choose a number from the menu. Try again.')


class MainOperation(Enum):
    """
    Defines end goals the user can achieve by running Infinium.
    """

    construct_model = 1
    add_database_entry = 2
    analyze_stock = 3
    exit = 4