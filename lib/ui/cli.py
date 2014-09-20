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
import argparse
from lib.consts import PROGRAM_NAME, STR_TO_MAIN_OPERATION, Developer
from lib.ui import base


# Module header.
__maintainer__ = Developer.JERRAD_GENSON
__contact__ = Developer.EMAIL[__maintainer__]


class CommandLineInterface(base.UserInterface):
    """
    User interface for running Infinium from the command line using command
    line arguments and a configuration file.

    Args
      cl_args: command line arguments from ``infinium.parse_command_line``.

    """

    def __init__(self, cl_args, configuration):
        self.__cl_args = cl_args
        self.__configuration = configuration

    @property
    def main_operation(self):
        return self.__cl_args.main_operation or self.__configuration.main_operation

    @property
    def model_path(self):
        return self.__cl_args.model_path or self.__configuration.model_path

    def show_test_results(self):
        raise NotImplementedError('`show_test_results` not yet implemented!')

    def show_error(self, message):
        print(message)


def launch_cli(cl_args, configuration):
    """
    Launch command line interface event loop.

    Args
      cl_args: Command line arguments from ``parse_command_line``.
      configuration: Configuration object from ``config.get_config``.

    Return
      None; does not return. Terminates program upon completion.

    """

    # Enter CLI event loop.
    while True:
        # Decide whether to analyze a stock, add a new entry to the database,
        # or construct a new valuation model.
        try:
            if user_interface.construct_model:
                construct_model()

            elif user_interface.load_model:
                load_model()

            elif user_interface.add_database_entry:
                raise NotImplementedError('`add_database_entry` operation not yet implemented.')

            elif user_interface.analyze_stock:
                raise NotImplementedError('`analyze_stock` operation not yet implemented.')

            elif user_interface.exit:
                sys.exit(consts.ExitCode.success)

        except ConfigFileCorruptError as error:
            logging.critical(error)
            user_interface.show_error(str(error))
            sys.exit(consts.ExitCode.config_file_corrupt)


def parse_command_line():
    """
    Parse command line arguments to Infinium.

    Return
      An instance of ``argparse.Namespace``.

    """

    class MainOperationAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, self.dest, STR_TO_MAIN_OPERATION[values])

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

    parser.add_argument('-m', '--main-operation',
                        help='What operation should {} perform?'.format(PROGRAM_NAME),
                        choices=STR_TO_MAIN_OPERATION,
                        dest='main_operation',
                        default=None,
                        action=MainOperationAction)

    cl_args = parser.parse_args()

    # TODO: Remove when GUI is ready to be used
    setattr(cl_args, 'graphical', False)

    return cl_args