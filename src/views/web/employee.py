#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Omnix System
# Copyright (C) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
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
    url = util.ensure_token()
    if url: return flask.redirect(url)

    return flask.render_template(
        "employee/list.html.tpl",
        link = "employees"
    )

@app.route("/employees.json", methods = ("GET",), json = True)
@quorum.ensure("foundation.employee.list")
def list_employees_json():
    url = util.ensure_token()
    if url: return flask.redirect(url)

    filter_string = quorum.get_field("filter_string", None)
    start_record = quorum.get_field("start_record", 0)
    number_records = quorum.get_field("number_records", 0)

    url = util.BASE_URL + "omni/employees.json"
    contents_s = util.get_json(
        url,
        filter_string = filter_string,
        start_record = start_record,
        number_records = number_records
    )

    return contents_s

@app.route("/employees/self", methods = ("GET",))
@quorum.ensure("foundation.employee.show.self")
def show_employee():
    url = util.ensure_token()
    if url: return flask.redirect(url)

    url = util.BASE_URL + "omni/employees/self.json"
    contents_s = util.get_json(url)

    return flask.render_template(
        "employee/show.html.tpl",
        link = "employees",
        sub_link = "info",
        is_self = True,
        employee = contents_s
    )

@app.route("/employees/self/sales", methods = ("GET",))
@quorum.ensure(("sales.sale_transaction.list.self", "sales.customer_return.list.self"))
def sales_employee():
    url = util.ensure_token()
    if url: return flask.redirect(url)

    url = util.BASE_URL + "omni/employees/self.json"
    contents_s = util.get_json(url)

    operations,\
    target_s,\
    sales_total,\
    sales_s,\
    returns_s,\
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
        employee = contents_s,
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

@app.route("/employees/<id>", methods = ("GET",))
@quorum.ensure("foundation.employee.show")
def show_employees(id):
    url = util.ensure_token()
    if url: return flask.redirect(url)

    url = util.BASE_URL + "omni/employees/%s.json" % id
    contents_s = util.get_json(url)

    return flask.render_template(
        "employee/show.html.tpl",
        link = "employees",
        sub_link = "info",
        employee = contents_s
    )

@app.route("/employees/<id>/sales", methods = ("GET",))
@quorum.ensure(("sales.sale_transaction.list", "sales.customer_return.list"))
def sales_employees(id):
    url = util.ensure_token()
    if url: return flask.redirect(url)

    url = util.BASE_URL + "omni/employees/%s.json" % id
    contents_s = util.get_json(url)

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
        employee = contents_s,
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
    now = datetime.datetime.utcnow()
    month = quorum.get_field("month", now.month, cast = int)
    year = quorum.get_field("year", now.year, cast = int)

    has_next = int("%04d%02d" % (year, month)) < int("%04d%02d" % (now.year, now.month))

    previous_month, previous_year = (month - 1, year) if not month == 1 else (12, year - 1)
    next_month, next_year = (month + 1, year) if not month == 12 else (1, year + 1)

    start_month, start_year = (month, year) if now.day >= 21 else (previous_month, previous_year)
    end_month, end_year = (start_month + 1, start_year) if not start_month == 12 else (1, start_year + 1)

    start = datetime.datetime(year = start_year, month = start_month, day = util.COMMISSION_DAY)
    end = datetime.datetime(year = end_year, month = end_month, day = util.COMMISSION_DAY)

    start_t = calendar.timegm(start.utctimetuple())
    end_t = calendar.timegm(end.utctimetuple())

    target = datetime.datetime(year = end_year, month = end_month, day = 1)
    target_s = target.strftime("%B %Y")

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
    if id: kwargs["filters[]"].append("primary_seller:equals:" + id)

    partial_url = "omni/sales.json" if id else "omni/sales/self.json"
    url = util.BASE_URL + partial_url
    sales_s = util.get_json(url, **kwargs)

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

    if id: kwargs["filters[]"].append("primary_return_processor:equals:" + id)

    partial_url = "omni/returns.json" if id else "omni/returns/self.json"
    url = util.BASE_URL + partial_url
    returns_s = util.get_json(url, **kwargs)

    operations = returns_s + sales_s

    sorter = lambda x, y: cmp(x["date"], y["date"])
    operations.sort(sorter, reverse = True)

    sales_total = 0
    for sale in sales_s: sales_total += sale["price"]["value"]
    for _return in returns_s: sales_total -= _return["price"]["value"]

    for operation in operations:
        date = operation["date"]
        date_t = datetime.datetime.utcfromtimestamp(date)
        operation["date_f"] = date_t.strftime("%b %d, %Y")

    return (
        operations,
        target_s,
        sales_total,
        sales_s,
        returns_s,
        previous_month,
        previous_year,
        next_month,
        next_year,
        has_next
    )
