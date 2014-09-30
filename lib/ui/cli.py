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
import re
import sys
import logging
from enum import Enum
from datetime import date
from getpass import getpass

# Third-party library imports.
from sqlalchemy.exc import OperationalError

# Infinium library imports.
import argparse
from lib import db
from lib.ml import construct_model
from lib.data import PROGRAM_NAME, Developer, ExitCode


__maintainer__ = Developer.JERRAD_GENSON
__contact__ = Developer.EMAIL[__maintainer__]


# Module constants
DOLLARS = '^\d*\.?\d{0,2}$'
YEARS = '^\d{4}$'
MONTHS = '^\d{1,2}$'
DAYS = '^\d{1,2}$'
RATIO = '^0*\.\d+$'

WELCOME_MESSAGE = """
Welcome to Infinium - cutting-edge stock valuation and analysis software.

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

    _show_welcome()

    # Connect to database.
    username = configuration.db_username
    password = configuration.db_password
    while True:
        try:
            db.connect_database(configuration.db_dialect,
                                configuration.db_driver,
                                username,
                                password,
                                configuration.db_host,
                                configuration.db_port,
                                configuration.db_database,
                                configuration.db_echo)

            break

        except OperationalError:
            logging.warning('Database credentials not valid.')
            username, password = _prompt_db_credentials(configuration.db_host,
                                                        configuration.db_port,
                                                        configuration.db_database)

    msg = 'Connected to database at {}:{}/{}'
    msg = msg.format(configuration.db_host,
                     configuration.db_port,
                     configuration.db_database)

    logging.info(msg)

    # Enter CLI event loop.
    while True:
        # Decide whether to analyze a stock, add a new entry to the database,
        # or construct a new valuation model.
        main_operation = _main_prompt()
        if main_operation is _MainOperation.construct_model:
            construct_model(configuration)

        elif main_operation is _MainOperation.add_database_entry:
            _add_database_entry()

        elif main_operation is _MainOperation.parse_annual_report:
            raise NotImplementedError()

        elif main_operation is _MainOperation.analyze_stock:
            raise NotImplementedError()

        elif main_operation is _MainOperation.exit:
            sys.exit(ExitCode.success.value)


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


def _show_welcome():
    """ Display Infinium welcome message. """

    print(WELCOME_MESSAGE)


def _main_prompt():
    """
    Prompt user to select main operation.

    Returns
      Instance of ``MainOperation``.

    """

    prompt = 'Choose one of the following numeric options:\n'
    prompt += '  1 - Construct model\n'
    prompt += '  2 - Add database entry\n'
    prompt += '  3 - Parse annual report\n'
    prompt += '  4 - Analyze stock\n'
    prompt += '  5 - Exit\n'
    prompt += '\nEnter selection: '
    return _prompt_until_valid(prompt,
                               type_=lambda x: _MainOperation(int(x)),
                               error='\nYou must choose a number from the menu. Try again.')


def _add_database_entry():
    """
    Event handler for `Add database entry`.
    """

    session = db.Session()
    company_id = _prompt_until_valid('\nEnter company ID: ')

    if not db.get_company_record(session, company_id):
        company_name = _prompt_until_valid('Enter company name: ')
        industries = db.get_industries(session)
        prompt = '\nWhich industry is this company in?\n'
        prompt += 'Choose a numeric selection from the options below.\n'
        for count, industry in enumerate(industries):
            prompt += '  {} - {}\n'.format(count+1, industry)

        new_industry = count + 2 if industries else 1
        prompt += '  {} - Add new industry\n'.format(new_industry)
        prompt += '\nEnter selection: '
        error = '\nYou must choose a number from the menu. Try again.'
        industry_id = _prompt_until_valid(prompt,
                                          type_=int,
                                          bounds=(1, new_industry+1),
                                          error=error)

        if industry_id == new_industry:
            industry_name = _prompt_until_valid('Enter new industry name: ')
            industry_table = db.Industry(name=industry_name)
            session.add(industry_table)
            session.commit()
            industry_id = db.get_industry_id(session, industry_name)

        company = db.Company(id=company_id,
                               industry_id=industry_id,
                               name=company_name)

        session.add(company)

    price = _prompt_until_valid('Enter the stock price: ',
                                type_=float,
                                pattern=DOLLARS,
                                nullable=True)

    year = _prompt_until_valid('Enter target year: ',
                               type_=int,
                               pattern=YEARS,
                               nullable=True)

    if price and year:
        month = _prompt_until_valid('Enter target month: ',
                                    type_=int,
                                    pattern=MONTHS)

        day = _prompt_until_valid('Enter target day: ',
                                  type_=int,
                                  pattern=DAYS)

        stock = db.Stock(company_id=company_id,
                         price=price,
                         date=date(year, month, day))

        session.add(stock)

    if year and not db.get_finance_record(session, company_id, year):
        _prompt_financials(session, company_id, year)

    session.commit()


def _prompt_financials(session, company_id, year):
        roe = _prompt_until_valid('Enter return on equity: ',
                                  type_=float,
                                  pattern=DOLLARS,
                                  nullable=True)

        if not roe:
            return

        npm = _prompt_until_valid('Enter net profit margin: ',
                                  type_=float,
                                  pattern=DOLLARS)

        net_sales = _prompt_until_valid('Enter net sales: ',
                                        type_=float,
                                        pattern=DOLLARS)

        net_income = _prompt_until_valid('Enter net income: ',
                                         type_=float,
                                         pattern=DOLLARS)

        epsg = _prompt_until_valid('Enter earnings per share growth: ',
                                   type_=float,
                                   pattern=DOLLARS)

        tca = _prompt_until_valid('Enter total current assets: ',
                                  type_=float,
                                  pattern=DOLLARS)

        tcl = _prompt_until_valid('Enter total current liabilities: ',
                                  type_=float,
                                  pattern=DOLLARS)

        fcf = _prompt_until_valid('Enter free cash flow: ',
                                  type_=float,
                                  pattern=DOLLARS)

        operating_margin = _prompt_until_valid('Enter operating margin: ',
                                               type_=float,
                                               pattern=DOLLARS)

        finances = db.Finances(company_id=company_id,
                               year=date(year, 1, 1),
                               return_on_equity=roe,
                               net_profit_margin=npm,
                               net_sales=net_sales,
                               net_income=net_income,
                               earnings_per_share_growth=epsg,
                               total_current_assets=tca,
                               total_current_liabilities=tcl,
                               free_cash_flow=fcf,
                               operating_margin=operating_margin)

        session.add(finances)


def _prompt_db_credentials(host, port, database):
    """
    Prompt user for their database access credentials.

    Args
      host: IP address of the database server.
      port: Port number of the database service.
      database: Name of the Infinium database.

    Return
      A tuple of (username, password).

    """

    print('\nDatabase connection failed.')
    print('Connecting to database at "{}:{}/{}"...'.format(host, port, database))
    username = input('Enter username: ')
    password = getpass('Enter password: ')

    return username, password


def _prompt_until_valid(prompt,
                        error=None,
                        type_=str,
                        input=input,
                        pattern='.+',
                        nullable=False,
                        bounds=None):
    """
    Prompt the user for input until it matches `type_`.
    """

    while True:
        try:
            user_input = input(prompt)
            if nullable and not user_input.strip():
                return None

            if not re.search(pattern, user_input):
                raise ValueError

            typed_input = type_(user_input)
            if bounds and not bounds[0] <= typed_input < bounds[1]:
                raise ValueError

            return typed_input

        except ValueError:
            if error:
                print(error)

            else:
                msg = 'Input must be of type `{}` and match pattern `{}`'
                msg = msg.format(type_.__name__, pattern)
                print(msg)


class _MainOperation(Enum):
    """
    Defines end goals the user can achieve by running Infinium.
    """

    construct_model = 1
    add_database_entry = 2
    parse_annual_report = 3
    analyze_stock = 4
    exit = 5