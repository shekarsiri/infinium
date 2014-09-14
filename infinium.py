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
from lib.ui.base import MainOperation
from lib.ui.cli import CommandLineInterface


# Module constants.
PROGRAM_NAME = 'Infinium'


def main():
    """
    Start Infinium's user interface and main event loop.

    Return
      None

    Raises
      NotImplementedError, SelectionError

    """

    # Parse command line arguments.
    cl_args = parse_command_line()

    # Launch user interface.
    if cl_args.graphical:
        # Use graphical user interface.
        raise NotImplementedError('GUI under construction. Please use CLI.')

    else:
        # Use command line interface.
        user_interface = CommandLineInterface(cl_args)
    
    # Enter main event loop.
    while True:
        # Decide whether to analyze a stock, add a new entry to the database, 
        # or construct a new valuation model.
        if user_interface.main_operation == MainOperation.construct_model:
            # Connect to database.
            database = connect_database(user_interface.database_type,
                                        user_interface.database_location)
            
            # Extract testing set from data.
            testing_data = extract_testing_data(database)
            
            if user_interface.load_model:
                # Load valuation model from disk.
                valuation_model = load_valuation_model(user_interface.model_path)
            
            else: 
                # Extract training set from data.
                training_data = extract_training_data(database)

                # Decide which classifier to use.
            
                # Construct the valuation model from training data.
                valuation_model = construct_valuation_model(training_data, classifier)
            
                # Save valuation model to disk.
                save_valuation_model(model_path)
            
            # Use testing data to evaluate quality of model.
            test_results = evaluate_model(valuation_model, testing_data)
            
            # Show results to user.
            user_interface.show_test_results(test_results)
            
        elif user_interface.main_operation == MainOperation.add_database_entry:
            pass
            
        elif user_interface.main_operation == MainOperation.analyze_stock:
            pass

        elif user_interface.main_operation == MainOperation.exit:
            sys.exit(0)
            
        else:
            # Invalid selection.
            msg = "'main_operation' attribute not defined by 'ui.EndGoal'."
            raise SelectionError(msg)


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