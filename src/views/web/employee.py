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

import util

from omnix import app
from omnix import flask
from omnix import quorum

@app.route("/employees", methods = ("GET",))
@quorum.ensure("foundation.employee.list")
def list_employees():
    url = util.ensure_api()
    if url: return flask.redirect(url)
    return flask.render_template(
        "employee/list.html.tpl",
        link = "employees"
    )

@app.route("/employees.json", methods = ("GET",), json = True)
@quorum.ensure("foundation.employee.list")
def list_employees_json():
    url = util.ensure_api()
    if url: return flask.redirect(url)
    api = util.get_api()
    object = quorum.get_object()
    return api.list_employees(**object)

@app.route("/employees/self", methods = ("GET",))
@quorum.ensure("foundation.employee.show.self")
def show_employee():
    url = util.ensure_api()
    if url: return flask.redirect(url)
    api = util.get_api()
    employee = api.self_employee()
    return flask.render_template(
        "employee/show.html.tpl",
        link = "employees",
        sub_link = "info",
        is_self = True,
        employee = employee
    )

@app.route("/employees/self/sales", methods = ("GET",))
@quorum.ensure(("sales.sale_transaction.list.self", "sales.customer_return.list.self"))
def sales_employee():
    url = util.ensure_api()
    if url: return flask.redirect(url)

    api = util.get_api()
    employee = api.self_employee()

    operations,\
    target,\
    sales_total,\
    sales,\
    returns,\
    previous_month,\
    previous_year,\
    next_month,\
    next_year,\
    has_next = get_sales()

    return flask.render_template(
        "employee/sales.html.tpl",
        link = "employees",
        sub_link = "sales",
        is_self = True,
        employee = employee,
        operations = operations,
        commission_rate = util.COMMISSION_RATE,
        title = target,
        sales_total = sales_total,
        sales_count = len(sales),
        returns_count = len(returns),
        previous = (previous_month, previous_year),
        next = (next_month, next_year),
        has_next = has_next
    )

@app.route("/employees/<int:id>", methods = ("GET",))
@quorum.ensure("foundation.employee.show")
def show_employees(id):
    url = util.ensure_api()
    if url: return flask.redirect(url)
    api = util.get_api()
    employee = api.get_employee(id)
    return flask.render_template(
        "employee/show.html.tpl",
        link = "employees",
        sub_link = "info",
        employee = employee
    )

@app.route("/employees/<int:id>/sales", methods = ("GET",))
@quorum.ensure(("sales.sale_transaction.list", "sales.customer_return.list"))
def sales_employees(id):
    url = util.ensure_api()
    if url: return flask.redirect(url)

    api = util.get_api()
    employee = api.get_employee(id)

    operations,\
    target_s,\
    sales_total,\
    sales_s,\
    returns_s,\
    previous_month,\
    previous_year,\
    next_month,\
    next_year,\
    has_next = get_sales(id = id)

    return flask.render_template(
        "employee/sales.html.tpl",
        link = "employees",
        sub_link = "sales",
        is_self = False,
        employee = employee,
        operations = operations,
        commission_rate = util.COMMISSION_RATE,
        title = target_s,
        sales_total = sales_total,
        sales_count = len(sales_s),
        returns_count = len(returns_s),
        previous = (previous_month, previous_year),
        next = (next_month, next_year),
        has_next = has_next
    )

def get_sales(id = None):
    api = util.get_api()

    now = datetime.datetime.utcnow()
    month = quorum.get_field("month", now.month, cast = int)
    year = quorum.get_field("year", now.year, cast = int)

    has_next = int("%04d%02d" % (year, month)) < int("%04d%02d" % (now.year, now.month))

    previous_month, previous_year = (month - 1, year) if not month == 1 else (12, year - 1)
    next_month, next_year = (month + 1, year) if not month == 12 else (1, year + 1)

    start_month, start_year = (month, year) if now.day >= util.COMMISSION_DAY else (previous_month, previous_year)
    end_month, end_year = (start_month + 1, start_year) if not start_month == 12 else (1, start_year + 1)

    start = datetime.datetime(year = start_year, month = start_month, day = util.COMMISSION_DAY)
    end = datetime.datetime(year = end_year, month = end_month, day = util.COMMISSION_DAY)

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
