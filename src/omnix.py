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

import json
import flask
import urllib
import urllib2
import datetime

import quorum

MONGO_DATABASE = "omnix"
""" The default database to be used for the connection with
the mongo database """

SECRET_KEY = "zhsga32ki5kvv7ymq8nolbleg248fzn1"
""" The "secret" key to be at the internal encryption
processes handled by flask (eg: sessions) """

CLIENT_ID = "0e8be9a3f87a4c6485878559b9abe282"
""" The id of the omni client to be used """

CLIENT_SECRET = "e484777ec81448d581c9293a0343cf55"
""" The secret key value to be used to access the
omni api as the client """

BASE_URL = "http://stage.hive:8080/dynamic/rest/mvc/"
""" The base url to be used to compose the various
complete url values for the various operations """

REDIRECT_URL = "http://localhost:8080/oauth"
""" The redirect base url to be used as the base value
for the construction of the base url instances """

SCOPE = (
    "foundation.store.list",
    "foundation.store.show",
    "foundation.employee.list",
    "foundation.employee.show",
    "foundation.supplier_company.list",
    "foundation.supplier_company.show",
    "customers.customer_person.list",
    "customers.customer_person.show",
    "analytics.sale_snapshot.list"
)
""" The list of permission to be used to create the
scope string for the oauth value """

app = flask.Flask(__name__)
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(31)
quorum.load(
    app,
    mongo_database = MONGO_DATABASE,
    name = "omnix.debug"
)

@app.route("/", methods = ("GET",))
@app.route("/index", methods = ("GET",))
def index():
    return flask.render_template(
        "index.html.tpl",
        link = "home"
    )

@app.route("/about", methods = ("GET",))
def about():
    access_token = flask.session.get("omnix.access_token", None)
    session_id = flask.session.get("omnix.session_id", None)

    return flask.render_template(
        "about.html.tpl",
        link = "about",
        access_token = access_token,
        session_id = session_id
    )

@app.route("/reset", methods = ("GET",))
def reset():
    _reset_session()

    return flask.render_template(
        "index.html.tpl",
        link = "home"
    )

@app.route("/oauth", methods = ("GET",))
def oauth():
    code = flask.request.args.get("code", None)

    error = flask.request.args.get("error", None)
    error_description = flask.request.args.get("error_description", None)
    if error: raise RuntimeError("%s - %s" % (error, error_description))

    url = BASE_URL + "omni/oauth/access_token"
    values = {
        "client_id" : CLIENT_ID,
        "client_secret" : CLIENT_SECRET,
        "grant_type" : "authorization_code",
        "redirect_uri" : REDIRECT_URL,
        "code" : code
    }

    contents_s = _post_data(url, values, authenticate = False, token = False)
    access_token = contents_s["access_token"]
    flask.session["omnix.access_token"] = access_token

    _ensure_session_id()

    return flask.redirect(
        flask.url_for("index")
    )

@app.route("/top", methods = ("GET",))
def top():
    access_token = flask.session.get("omnix.access_token", None)
    session_id = flask.session.get("omnix.session_id", None)

    return flask.render_template(
        "top.html.tpl",
        link = "top",
        access_token = access_token,
        session_id = session_id
    )

@app.route("/reports", methods = ("GET",))
def reports():
    return flask.render_template(
        "reports.html.tpl",
        link = "reports"
    )

@app.route("/reports/sales", methods = ("GET",))
def sales_reports():
    return flask.render_template(
        "reports_sales.html.tpl",
        link = "reports"
    )

@app.route("/customers", methods = ("GET",))
def list_customers():
    url = _ensure_token()
    if url: return flask.redirect(url)

    return flask.render_template(
        "customers_list.html.tpl",
        link = "customers"
    )

@app.route("/customers.json", methods = ("GET",))
def list_customers_json():
    url = _ensure_token()
    if url: return flask.redirect(url)

    filter_string = flask.request.args.get("filter_string", None)
    start_record = flask.request.args.get("start_record", 0)
    number_records = flask.request.args.get("number_records", 0)

    values = {
        "filter_string" : filter_string,
        "start_record" : start_record,
        "number_records" : number_records
    }

    url = BASE_URL + "omni/customer_persons.json"
    contents_s = _get_data(url, values)

    return json.dumps(contents_s)

@app.route("/customers/<id>", methods = ("GET",))
def show_customers(id):
    url = _ensure_token()
    if url: return flask.redirect(url)

    url = BASE_URL + "omni/customer_persons/%s.json" % id
    contents_s = _get_data(url)

    return flask.render_template(
        "customers_show.html.tpl",
        link = "customers",
        customer = contents_s
    )

@app.route("/suppliers", methods = ("GET",))
def list_suppliers():
    url = _ensure_token()
    if url: return flask.redirect(url)

    return flask.render_template(
        "suppliers_list.html.tpl",
        link = "suppliers"
    )

@app.route("/suppliers.json", methods = ("GET",))
def list_suppliers_json():
    url = _ensure_token()
    if url: return flask.redirect(url)

    filter_string = flask.request.args.get("filter_string", None)
    start_record = flask.request.args.get("start_record", 0)
    number_records = flask.request.args.get("number_records", 0)

    values = {
        "filter_string" : filter_string,
        "start_record" : start_record,
        "number_records" : number_records
    }

    url = BASE_URL + "omni/supplier_companies.json"
    contents_s = _get_data(url, values)

    return json.dumps(contents_s)

@app.route("/suppliers/<id>", methods = ("GET",))
def show_suppliers(id):
    url = _ensure_token()
    if url: return flask.redirect(url)

    url = BASE_URL + "omni/supplier_companies/%s.json" % id
    contents_s = _get_data(url)

    return flask.render_template(
        "suppliers_show.html.tpl",
        link = "suppliers",
        supplier = contents_s
    )

@app.route("/stores", methods = ("GET",))
def list_stores():
    url = _ensure_token()
    if url: return flask.redirect(url)

    return flask.render_template(
        "stores_list.html.tpl",
        link = "stores"
    )

@app.route("/stores.json", methods = ("GET",))
def list_stores_json():
    url = _ensure_token()
    if url: return flask.redirect(url)

    filter_string = flask.request.args.get("filter_string", None)
    start_record = flask.request.args.get("start_record", 0)
    number_records = flask.request.args.get("number_records", 0)

    values = {
        "filter_string" : filter_string,
        "start_record" : start_record,
        "number_records" : number_records
    }

    url = BASE_URL + "omni/stores.json"
    contents_s = _get_data(url, values)

    return json.dumps(contents_s)

@app.route("/stores/<id>", methods = ("GET",))
def show_stores(id):
    url = _ensure_token()
    if url: return flask.redirect(url)

    url = BASE_URL + "omni/stores/%s.json" % id
    contents_s = _get_data(url)

    return flask.render_template(
        "stores_show.html.tpl",
        link = "stores",
        sub_link = "info",
        store = contents_s
    )

@app.route("/stores/<id>/sales", methods = ("GET",))
def sales_stores(id):
    url = _ensure_token()
    if url: return flask.redirect(url)

    now = datetime.datetime.utcnow()
    current_day = datetime.datetime(now.year, now.month, now.day)

    id_s = str(id)

    url = BASE_URL + "omni/stores/%s.json" % id
    contents_s = _get_data(url)
    store_s = contents_s

    url = BASE_URL + "omni/sale_snapshots/stats.json"
    values = {
        "unit" : "day",
        "store_id" : id_s
    }
    contents_s = _get_data(url, values = values)
    stats_s = contents_s[id_s]
    current_s = {
        "amount_price_vat" : stats_s["amount_price_vat"][-1],
        "number_sales" : stats_s["number_sales"][-1],
        "date" : current_day
    }

    days_s = []

    count = len(stats_s["amount_price_vat"]) - 1
    count_r = range(count)
    count_r.reverse()
    _current_day = current_day
    for index in count_r:
        _current_day -= datetime.timedelta(1)
        day =  {
            "amount_price_vat" : stats_s["amount_price_vat"][index],
            "number_sales" : stats_s["number_sales"][index],
            "date" : _current_day
        }
        days_s.append(day)

    return flask.render_template(
        "stores_sales.html.tpl",
        link = "stores",
        sub_link = "sales",
        store = store_s,
        stats = stats_s,
        current = current_s,
        days = days_s
    )

@app.route("/employees", methods = ("GET",))
def list_employees():
    url = _ensure_token()
    if url: return flask.redirect(url)

    return flask.render_template(
        "employees_list.html.tpl",
        link = "employees"
    )

@app.route("/employees.json", methods = ("GET",))
def list_employees_json():
    url = _ensure_token()
    if url: return flask.redirect(url)

    filter_string = flask.request.args.get("filter_string", None)
    start_record = flask.request.args.get("start_record", 0)
    number_records = flask.request.args.get("number_records", 0)

    values = {
        "filter_string" : filter_string,
        "start_record" : start_record,
        "number_records" : number_records
    }

    url = BASE_URL + "omni/employees.json"
    contents_s = _get_data(url, values)

    return json.dumps(contents_s)

@app.route("/employees/<id>", methods = ("GET",))
def show_employees(id):
    url = _ensure_token()
    if url: return flask.redirect(url)

    url = BASE_URL + "omni/employees/%s.json" % id
    contents_s = _get_data(url)

    return flask.render_template(
        "employees_show.html.tpl",
        link = "employees",
        sub_link = "info",
        employee = contents_s
    )

@app.route("/employees/<id>/sales", methods = ("GET",))
def sales_employees(id):
    url = _ensure_token()
    if url: return flask.redirect(url)

    url = BASE_URL + "omni/employees/%s.json" % id
    contents_s = _get_data(url)

    return flask.render_template(
        "employees_sales.html.tpl",
        link = "employees",
        sub_link = "sales",
        employee = contents_s
    )

@app.errorhandler(404)
def handler_404(error):
    return str(error)

@app.errorhandler(413)
def handler_413(error):
    return str(error)

@app.errorhandler(BaseException)
def handler_exception(error):
    return str(error)

def _get_data(url, values = None, authenticate = True, token = False):
    # starts the variable holding the number of
    # retrieves to be used
    retries = 5

    while True:
        try:
            return __get_data(url, values, authenticate, token)
        except urllib2.HTTPError, error:
            data = error.read()
            data_s = json.loads(data)
            exception = data_s.get("exception", {})
            exception_name = exception.get("exception_name", None)
            message = exception.get("message", None)
            if exception_name == "ControllerValidationReasonFailed":
                _reset_session_id()
            elif exception_name:
                raise RuntimeError("%s - %s" % (exception_name, message))
            else: raise

        # decrements the number of retries and checks if the
        # number of retries has reached the limit
        retries -= 1
        if retries == 0: raise RuntimeError("data retrieval not possible")

def _post_data(url, values = None, authenticate = True, token = False):
    # starts the variable holding the number of
    # retrieves to be used
    retries = 5

    while True:
        try:
            return __post_data(url, values, authenticate, token)
        except urllib2.HTTPError, error:
            data = error.read()
            data_s = json.loads(data)
            exception = data_s.get("exception", {})
            exception_name = exception.get("exception_name", None)
            message = exception.get("message", None)
            if exception_name == "ControllerValidationReasonFailed":
                _reset_session_id()
            elif exception_name:
                raise RuntimeError("%s - %s" % (exception_name, message))
            else: raise

        # decrements the number of retries and checks if the
        # number of retries has reached the limit
        retries -= 1
        if retries == 0: raise RuntimeError("data retrieval not possible")

def __get_data(url, values = None, authenticate = True, token = False):
    values = values or {}
    if authenticate: values["session_id"] = flask.session["omnix.session_id"]
    if token: values["access_token"] = flask.session["omnix.access_token"]
    data = urllib.urlencode(values)
    url = url + "?" + data
    response = urllib2.urlopen(url)
    contents = response.read()
    contents_s = json.loads(contents)
    return contents_s

def __post_data(url, values = None, authenticate = True, token = False):
    values = values or {}
    if authenticate: values["session_id"] = flask.session["omnix.session_id"]
    if token: values["access_token"] = flask.session["omnix.access_token"]
    data = urllib.urlencode(values)
    request = urllib2.Request(url, data)
    response = urllib2.urlopen(request)
    contents = response.read()
    contents_s = json.loads(contents)
    return contents_s

def _ensure_token():
    access_token = flask.session.get("omnix.access_token", None)
    if access_token: _ensure_session_id(); return None

    url = BASE_URL + "omni_web_adm/oauth/authorize"
    values = {
        "client_id" : CLIENT_ID,
        "redirect_uri" : REDIRECT_URL,
        "response_type" : "code",
        "scope" : " ".join(SCOPE)
    }

    data = urllib.urlencode(values)
    url = url + "?" + data
    return url

def _ensure_session_id():
    session_id = flask.session.get("omnix.session_id", None)
    if session_id: return None

    url = BASE_URL + "omni/oauth/start_session"
    contents_s = _get_data(url, authenticate = False, token = True)
    session_id = contents_s.get("_session_id", None)
    flask.session["omnix.session_id"] = session_id

def _reset_session():
    if "omnix.access_token" in flask.session: del flask.session["omnix.access_token"]
    if "omnix.session_id" in flask.session: del flask.session["omnix.session_id"]
    flask.session.modified = True

def _reset_session_id():
    if "omnix.session_id" in flask.session:
        del flask.session["omnix.session_id"]
    if "omnix.access_token" in flask.session:
        del flask.session["omnix.access_token"]
    flask.session.modified = True
    _ensure_session_id()

def run():
    # sets the debug control in the application
    # then checks the current environment variable
    # for the target port for execution (external)
    # and then start running it (continuous loop)
    debug = quorum.conf("DEBUG", False) and True or False
    reloader = quorum.conf("RELOADER", False) and True or False
    port = int(quorum.conf("PORT", 5000))
    app.debug = debug
    app.secret_key = SECRET_KEY
    app.run(
        use_debugger = debug,
        debug = debug,
        use_reloader = reloader,
        host = "0.0.0.0",
        port = port
    )

if __name__ == "__main__":
    run()
