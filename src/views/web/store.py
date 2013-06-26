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

import datetime

import util

from omnix import app
from omnix import flask
from omnix import quorum

@app.route("/stores", methods = ("GET",))
@quorum.ensure("foundation.store.list")
def list_stores():
    url = util.ensure_token()
    if url: return flask.redirect(url)

    return flask.render_template(
        "store/list.html.tpl",
        link = "stores"
    )

@app.route("/stores.json", methods = ("GET",), json = True)
@quorum.ensure("foundation.store.list")
def list_stores_json():
    url = util.ensure_token()
    if url: return flask.redirect(url)

    filter_string = quorum.get_field("filter_string", None)
    start_record = quorum.get_field("start_record", 0)
    number_records = quorum.get_field("number_records", 0)

    url = util.BASE_URL + "omni/stores.json"
    contents_s = util.get_json(
        url,
        filter_string = filter_string,
        start_record = start_record,
        number_records = number_records
    )

    return contents_s

@app.route("/stores/<id>", methods = ("GET",))
@quorum.ensure("foundation.store.show")
def show_stores(id):
    url = util.ensure_token()
    if url: return flask.redirect(url)

    url = util.BASE_URL + "omni/stores/%s.json" % id
    contents_s = util.get_json(url)

    return flask.render_template(
        "store/show.html.tpl",
        link = "stores",
        sub_link = "info",
        store = contents_s
    )

@app.route("/stores/<id>/sales", methods = ("GET",))
def sales_stores(id):
    url = util.ensure_token()
    if url: return flask.redirect(url)

    now = datetime.datetime.utcnow()
    current_day = datetime.datetime(now.year, now.month, now.day)

    id_s = str(id)

    url = util.BASE_URL + "omni/stores/%s.json" % id
    contents_s = util.get_json(url)
    store_s = contents_s

    url = util.BASE_URL + "omni/sale_snapshots/stats.json"
    contents_s = util.get_json(url, unit = "day", store_id = id_s)
    stats_s = contents_s[id_s]
    current_s = dict(
        amount_price_vat = stats_s["amount_price_vat"][-1],
        number_sales = stats_s["number_sales"][-1],
        date = current_day
    )

    days_s = []

    count = len(stats_s["amount_price_vat"]) - 1
    count_r = range(count)
    count_r.reverse()
    _current_day = current_day
    for index in count_r:
        _current_day -= datetime.timedelta(1)
        day = dict(
            amount_price_vat = stats_s["amount_price_vat"][index],
            number_sales = stats_s["number_sales"][index],
            date = _current_day
        )
        days_s.append(day)

    previous_s = days_s[0] if days_s else dict()
    current_s["amount_delta"] = current_s["amount_price_vat"] -\
        previous_s.get("amount_price_vat", 0)
    current_s["number_delta"] = current_s["number_sales"] -\
        previous_s.get("number_sales", 0)

    if current_s["amount_delta"] == 0: current_s["amount_direction"] = "equal"
    elif current_s["amount_delta"] > 0: current_s["amount_direction"] = "up"
    else: current_s["amount_direction"] = "down"

    if current_s["number_delta"] == 0: current_s["number_direction"] = "equal"
    elif current_s["number_delta"] > 0: current_s["number_direction"] = "up"
    else: current_s["number_direction"] = "down"

    return flask.render_template(
        "store/sales.html.tpl",
        link = "stores",
        sub_link = "sales",
        store = store_s,
        stats = stats_s,
        current = current_s,
        days = days_s
    )
