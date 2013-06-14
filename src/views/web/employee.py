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

import util

from omnix import app
from omnix import flask
from omnix import quorum

@app.route("/employees", methods = ("GET",))
def list_employees():
    url = util.ensure_token()
    if url: return flask.redirect(url)

    return flask.render_template(
        "employee/list.html.tpl",
        link = "employees"
    )

@app.route("/employees.json", methods = ("GET",), json = True)
def list_employees_json():
    url = util.ensure_token()
    if url: return flask.redirect(url)

    filter_string = quorum.get_field("filter_string", None)
    start_record = quorum.get_field("start_record", 0)
    number_records = quorum.get_field("number_records", 0)

    values = {
        "filter_string" : filter_string,
        "start_record" : start_record,
        "number_records" : number_records
    }

    url = util.BASE_URL + "omni/employees.json"
    contents_s = util.get_json(url, values)

    return contents_s

@app.route("/employees/<id>", methods = ("GET",))
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
def sales_employees(id):
    url = util.ensure_token()
    if url: return flask.redirect(url)

    url = util.BASE_URL + "omni/employees/%s.json" % id
    contents_s = util.get_json(url)

    return flask.render_template(
        "employees_sales.html.tpl",
        link = "employees",
        sub_link = "sales",
        employee = contents_s
    )
