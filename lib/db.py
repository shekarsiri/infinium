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

# Third-party imports.
from sqlalchemy import Column, String, ForeignKey, Enum, null, Date, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# Infinium library imports.
from lib import data


# Module header.
__maintainer__ = data.Developer.JERRAD_GENSON
__contact__ = data.Developer.EMAIL[__maintainer__]


# Module constants.
_Base = declarative_base()


class Companies(_Base):
    __tablename__ = 'companies'
    id = Column(String, primary_key=True)
    data_set_type = Column(Enum('train', 'test'), nullable=True, default=null)


class Finances(_Base):
    __tablename__ = 'finances'
    company = relationship(Companies, backref=backref('finances', uselist=True))
    company_id = Column(String, ForeignKey('companies.id'), primary_key=True)
    year = Column(Date, primary_key=True)
    return_on_equity = Column(Float)
    net_profit_margin = Column(Float)
    net_sales = Column(Float)
    net_income = Column(Float)
    earnings_per_share_growth = Column(Float)
    total_current_assets = Column(Float)
    total_current_liabilities = Column(Float)
    free_cash_flow = Column(Float)
    operating_margin = Column(Float)


class StockPrices(_Base):
    __tablename__ = 'stock_prices'
    company = relationship(Companies, backref=backref('stock_prices', uselist=True))
    company_id = Column(String, ForeignKey('companies.id'), primary_key=True)
    date = Column(Date, primary_key=True)
    price = Column(Float)
    valuation = Column(Enum('accurate', 'low', 'very_low'), nullable=True, default=null)