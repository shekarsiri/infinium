"""
Interface to Infinium database systems.

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
from datetime import date

# Third-party imports.
from sqlalchemy import Column, String, ForeignKey, Integer, Date, Float, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Infinium library imports.
from lib import data


# Module header.
__maintainer__ = data.Developer.JERRAD_GENSON
__contact__ = data.Developer.EMAIL[__maintainer__]


# Module constants.
_Base = declarative_base()


def get_finance_record(session, company_id, year):
    """
    Get a record from the Finances table.

    Args
      session: The Session object to query.
      company_id: ID of the company whose record to extract.
      year: Year of the record to extract as an integer.

    Return
      Record of the given company's finances at the given year, or None if no
      such record exists.

    """

    for finances in session.query(Finances).filter(Finances.company_id == company_id, Finances.year == date(year, 1, 1)):

        return finances


def get_company_record(session, company_id):
    """
    Get a record from the Companies table.

    Args
      session: The session object to query.
      company_id: ID of the company whose record to extract.

    Return
      Company record of the given ``company_id``.

    """

    for company in session.query(Company).filter(Company.id == company_id):
        return company


def extract_training_data(database):
    raise NotImplementedError('`extract_training_data` operation not yet implemented.')


def connect_database(dialect, driver, username, password, host, port, database,
                     echo=False):
    """
    Connect to the Infinium database. ``Session`` may be instantiated only
    after successfully calling this function.

    Args
      dialect: The database dialect (e.g. 'postgresql').
      driver: The database driver (e.g. 'psycopg2').
      username: Database access credentials username.
      password: Database access credentials password.
      host: IP address of the database host machine.
      port: Which port the database service is listening on.
      database: Name of the database.
      echo: ``True`` to make database queries in verbose mode.

    Returns
      None

    """

    global Session

    url = '{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}'
    url = url.format(dialect=dialect,
                     driver=driver,
                     username=username,
                     password=password,
                     host=host,
                     port=port,
                     database=database)

    engine = create_engine(url, echo=echo)
    _Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)


def get_industries(session):
    """
    Return list of industries from database, ordered by ``industry_id``.
    """

    industries = session.query(Industry).all()
    return [x.name for x in sorted(industries, key=lambda x: x.id)]


def get_industry_id(session, name):
    """
    Return ``id`` of the corresponding industry ``name``.
    """

    return session.query(Industry).filter(Industry.name == name).add_column('id').first().id


class Industry(_Base):
    __tablename__ = 'industries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)


class Company(_Base):
    __tablename__ = 'companies'
    industry = relationship(Industry, backref=backref('industries', uselist=True))
    id = Column(String, primary_key=True)
    industry_id = Column(ForeignKey('industries.id'), nullable=False)
    name = Column(String, nullable=False)


class Finances(_Base):
    __tablename__ = 'finances'
    company = relationship(Company, backref=backref('finances', uselist=True))
    company_id = Column(String, ForeignKey('companies.id'), primary_key=True)
    year = Column(Date, primary_key=True)
    return_on_equity = Column(Float, nullable=False)
    net_profit_margin = Column(Float, nullable=False)
    net_sales = Column(Float, nullable=False)
    net_income = Column(Float, nullable=False)
    earnings_per_share_growth = Column(Float, nullable=False)
    total_current_assets = Column(Float, nullable=False)
    total_current_liabilities = Column(Float, nullable=False)
    free_cash_flow = Column(Float, nullable=False)
    operating_margin = Column(Float, nullable=False)


class Stock(_Base):
    __tablename__ = 'stocks'
    company = relationship(Company, backref=backref('stocks', uselist=True))
    company_id = Column(String, ForeignKey('companies.id'), primary_key=True)
    date = Column(Date, primary_key=True)
    price = Column(Float, nullable=False)
    earnings_per_share = Column(Float, nullable=False)
    dividend = Column(Float, nullable=False)
    dividend_payout_ratio = Column(Float, nullable=False)
    intrinsic_value = Column(Float)


class Session:
    """
    Do not instantiate this class. You must call ``connect_database`` first.
    """

    def __init__(self):
        raise SessionNotDefinedError('No database has been connected.')


class SessionNotDefinedError(Exception):
    """
    Indicates a `Session` instance was created before `connect_database` was called.

    """

    pass