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

# Python standard library imports.
import sys
import logging
from os import getenv

# Infinium library imports.
from lib import consts
from lib.ui.base import SelectionError
from lib.ui.cli import CommandLineInterface, parse_command_line
from lib.ui.config import get_config, ConfigFileNotFoundError


# Module header.
__maintainer__ = consts.Developer.JERRAD_GENSON
__contact__ = consts.Developer.EMAIL[__maintainer__]


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

    # Configure root Logger.
    configure_logging(cl_args)

    # Get configuration options.
    try:
        configuration = get_config()

    except ConfigFileNotFoundError as config_file_not_found_error:
        configuration = None
        logging.critical(config_file_not_found_error)

    # Launch user interface.
    if cl_args.graphical:
        # Use graphical user interface.
        raise NotImplementedError('GUI under construction. Please use CLI.')

    else:
        # Use command line interface.
        user_interface = CommandLineInterface(cl_args, configuration)

    if not configuration:
        msg = 'Critical error: the configuration file could not be found. '
        msg += '{} will now exit.'.format(consts.PROGRAM_NAME)
        user_interface.show_error(msg)
        sys.exit(consts.ExitCode.config_file_not_found)
    
    # Enter main event loop.
    while True:
        # Decide whether to analyze a stock, add a new entry to the database, 
        # or construct a new valuation model.
        if user_interface.main_operation == consts.MainOperation.construct_model:
            raise NotImplementedError('`construct_model` operation not yet implemented.')

            # Connect to database.
            database = connect_database(configuration.database_type,
                                        configuration.database_path)
            
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
            
        elif user_interface.main_operation == consts.MainOperation.add_database_entry:
            raise NotImplementedError('`add_database_entry` operation not yet implemented.')
            
        elif user_interface.main_operation == consts.MainOperation.analyze_stock:
            raise NotImplementedError('`analyze_stock` operation not yet implemented.')

        elif user_interface.main_operation == consts.MainOperation.exit:
            sys.exit(consts.ExitCode.success)
            
        else:
            # Invalid selection.
            msg = '`{}` not defined by `MainOperation`.'.format(user_interface.main_operation)
            raise SelectionError(msg)


def configure_logging(cl_args):
    """
    Configure root Logger for Infinium.

    Args
      cl_args: A namespace created by ``argparse``.

    Returns
      None

    """

    # Configure logger.
    log_dir = getenv(consts.LOG_VAR, consts.DEFAULT_LOG_PATH)
    log_path = str(log_dir / consts.LOG_FILE_NAME)
    log_level = logging.DEBUG if cl_args.debug else logging.INFO
    logging.basicConfig(filename=log_path, level=log_level)

    if cl_args.verbose:
        root = logging.getLogger()
        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setLevel(log_level)
        root.addHandler(stream_handler)


if __name__ == '__main__':
    main()