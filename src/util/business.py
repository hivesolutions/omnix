#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Omnix System
# Copyright (C) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Omnix System.
#
# Hive Omnix System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Omnix System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Omnix System. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import calendar
import datetime

from util import config
from util import logic

def get_sales(id = None, year = None, month = None):
    api = logic.get_api()

    now = datetime.datetime.utcnow()
    year = year or now.year
    month = month or now.month

    has_next = int("%04d%02d" % (year, month)) < int("%04d%02d" % (now.year, now.month))

    previous_month, previous_year = (month - 1, year) if not month == 1 else (12, year - 1)
    next_month, next_year = (month + 1, year) if not month == 12 else (1, year + 1)

    start_month, start_year = (month, year) if now.day >= config.COMMISSION_DAY else (previous_month, previous_year)
    end_month, end_year = (start_month + 1, start_year) if not start_month == 12 else (1, start_year + 1)

    start = datetime.datetime(
        year = start_year,
        month = start_month,
        day = config.COMMISSION_DAY
    )
    end = datetime.datetime(
        year = end_year,
        month = end_month,
        day = config.COMMISSION_DAY
    )

    start_t = calendar.timegm(start.utctimetuple())
    end_t = calendar.timegm(end.utctimetuple())

    target = datetime.datetime(year = end_year, month = end_month, day = 1)
    target = target.strftime("%B %Y")

    kwargs = {
        "filter_string" : "",
        "start_record" : 0,
        "number_records" : -1,
        "sort" : "date:descending",
        "filters[]" : [
            "date:greater:" + str(start_t),
            "date:lesser:" + str(end_t)
        ]
    }
    if id: kwargs["filters[]"].append("primary_seller:equals:" + str(id))
    sales = api.list_sales(**kwargs) if id else api.self_sales(**kwargs)

    kwargs = {
        "filter_string" : "",
        "start_record" : 0,
        "number_records" : -1,
        "sort" : "date:descending",
        "filters[]" : [
            "date:greater:" + str(start_t),
            "date:lesser:" + str(end_t)
        ]
    }

    if id: kwargs["filters[]"].append("primary_return_processor:equals:" + str(id))
    returns = api.list_returns(**kwargs) if id else api.self_returns(**kwargs)

    operations = returns + sales

    sorter = lambda x, y: x["date"] - y["date"]
    operations.sort(sorter, reverse = True)

    sales_total = 0
    for sale in sales: sales_total += sale["price"]["value"]
    for _return in returns: sales_total -= _return["price"]["value"]

    for operation in operations:
        date = operation["date"]
        date_t = datetime.datetime.utcfromtimestamp(date)
        operation["date_f"] = date_t.strftime("%b %d, %Y")

    return (
        operations,
        target,
        sales_total,
        sales,
        returns,
        previous_month,
        previous_year,
        next_month,
        next_year,
        has_next
    )
