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

from omnix import util

from omnix.main import app
from omnix.main import flask
from omnix.main import quorum

@app.route("/suppliers", methods = ("GET",))
def list_suppliers():
    url = util.ensure_api()
    if url: return flask.redirect(url)
    return flask.render_template(
        "supplier/list.html.tpl",
        link = "suppliers"
    )

@app.route("/suppliers.json", methods = ("GET",), json = True)
def list_suppliers_json():
    url = util.ensure_api()
    if url: return flask.redirect(url)
    api = util.get_api()
    object = quorum.get_object()
    return api.list_companies(**object)

@app.route("/suppliers/<int:id>", methods = ("GET",))
def show_suppliers(id):
    url = util.ensure_api()
    if url: return flask.redirect(url)
    api = util.get_api()
    supplier = api.get_company(id)
    return flask.render_template(
        "supplier/show.html.tpl",
        link = "suppliers",
        supplier = supplier
    )
