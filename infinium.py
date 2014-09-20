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
from lib.ui.cli import parse_command_line, launch_cli
from lib.ui.config import get_config, ConfigurationError


# Module header.
__maintainer__ = consts.Developer.JERRAD_GENSON
__contact__ = consts.Developer.EMAIL[__maintainer__]


def main():
    """
    Parse command line, read configuration file, and launch Infinium's user
    interface.

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

    except (ConfigurationError, OSError) as error:
        logging.critical(error)
        print(error, sys.stderr)
        sys.exit(consts.ExitCode.config_file_not_found)

    # Launch user interface.
    if cl_args.graphical:
        # Use graphical user interface.
        raise NotImplementedError('GUI under construction. Please use CLI.')

    else:
        # Use command line interface.
        launch_cli(cl_args, configuration)


def configure_logging(cl_args):
    """
    Configure root Logger for Infinium.

    Args
      cl_args: A namespace created by ``argparse``.

    Returns
      None

    """

    log_dir = getenv(consts.LOG_VAR, consts.DEFAULT_LOG_PATH)
    log_path = str(log_dir / consts.LOG_FILE_NAME)
    log_level = logging.DEBUG if cl_args.debug else logging.INFO
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s',
                                  datefmt='%m/%d/%Y %I:%M:%S %p')

    root = logging.getLogger()
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)
    if cl_args.verbose:
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(log_level)
        stderr_handler.setFormatter(formatter)
        root.addHandler(stderr_handler)


def connect_database(configuration):
    """
    Decide which database to use and connect to it.

    Args
      configuration: The configuration object from ``lib.ui.config``.

    Returns
      An instance of ``lib.db.base.Database``.

    """

    if configuration.database_type == consts.DatabaseType.pgsql:
        # Connect to PostgreSQL database.
        database = PostgresDatabase(configuration.database_path)

    return database


def evaluate_model(valuation_model, testing_data):
    raise NotImplementedError('`evaluate_model` operation not yet implemented.')


def extract_training_data(database):
    raise NotImplementedError('`extract_training_data` operation not yet implemented.')


def save_model(valuation_model, path):
    raise NotImplementedError('`save_valuation_model` operation not yet implemented.')


def load_model(path):
    raise NotImplementedError('`load_valuation_model` operation not yet implemented.')


def construct_model(training_data, classifier):
    raise NotImplementedError('`construct_model` operation not yet implemented.')


if __name__ == '__main__':
    main()