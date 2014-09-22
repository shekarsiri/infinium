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

# Infinium library imports.
from lib import data
from lib.ui.cli import parse_command_line, launch_cli
from lib.ui.config import get_config, ConfigurationError


# Module header.
__maintainer__ = data.Developer.JERRAD_GENSON
__contact__ = data.Developer.EMAIL[__maintainer__]


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

    # Get configuration options.
    try:
        configuration = get_config()

    except (ConfigurationError, OSError) as error:
        print(error, sys.stderr)
        sys.exit(data.ExitCode.config_file_not_found)

    # Configure root Logger.
    configure_logging(cl_args, configuration)

    # Launch user interface.
    if cl_args.graphical:
        # Use graphical user interface.
        raise NotImplementedError('GUI under construction. Please use CLI.')

    else:
        # Use command line interface.
        launch_cli(configuration)


def configure_logging(cl_args, configuration):
    """
    Configure root Logger for Infinium.

    Args
      cl_args: A namespace created by ``argparse``.

    Returns
      None

    """

    log_level = logging.DEBUG if cl_args.debug else logging.INFO
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s',
                                  datefmt='%m/%d/%Y %I:%M:%S %p')

    root = logging.getLogger()
    file_handler = logging.FileHandler(str(configuration.log_path))
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)
    if cl_args.verbose:
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(log_level)
        stderr_handler.setFormatter(formatter)
        root.addHandler(stderr_handler)


if __name__ == '__main__':
    main()