"""
Infinium's main controller module. Execution begins here.

Contains command line parser and ``main`` function, which controls overall
program flow and is where execution begins.

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
import argparse
import sys

# Infinium library imports.
from lib.ui.base import EndGoal
from lib.ui.cli import CLI


# Module constants.
PROGRAM_NAME = 'Infinium'


def main():
    """
    Start Infinium's main control flow routine.

    Returns:
      None

    Raises:
      NotImplementedError, SelectionError

    """

    # Parse command line arguments.
    cl_args = parse_command_line()
    if cl_args.graphical:
        # Use graphical user interface.
        raise NotImplementedError('GUI under construction. Please use CLI.')

    else:
        # Use command line interface.
        user_interface = CLI(cl_args)

    # Launch user interface.
    
    # Enter main event loop.
    while True:
        # Decide whether to analyze a stock, add a new entry to the database, 
        # or construct a new valuation model.
        if user_interface.end_goal == EndGoal.construct_model:
            # Connect to database.
            
            # Extract testing set from data.
            
            if user_interface.load_model:
                # Load valuation model from disk.
                pass   
            
            else: 
                # Extract training set from data.
            
                # Construct the valuation model from training data.
            
                # Save model parameters to disk.
                pass
            
            # Use testing data to evaluate quality of model.
            
            # Save testing results to disk.
            
        elif user_interface.end_goal == EndGoal.add_database_entry:
            pass
            
        elif user_interface.end_goal == EndGoal.analyze_stock:
            pass

        elif user_interface.end_goal == EndGoal.exit:
            sys.exit(0)
            
        else:
            # Invalid selection.
            msg = "'end_goal' attribute not defined by 'ui.EndGoal'."
            raise SelectionError(msg)


def parse_command_line():
    """
    Parse command line arguments to Infinium.

    Returns:
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

    parser.add_argument('-g', '--graphical',
                        help='Launch {} with GUI. Note: currently not functional.'.format(PROGRAM_NAME),
                        action='store_true',
                        dest='graphical')

    cl_args = parser.parse_args()

    return cl_args


class SelectionError(Exception):
    """
    Raised when an instance of UserInterface specifies an invalid selection.
    """

    pass


if __name__ == '__main__':
    main()