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

import urllib

import config

from omnix import flask
from omnix import quorum

def get_json(url, authenticate = True, token = False, **kwargs):
    if authenticate: kwargs["session_id"] = flask.session["omnix.session_id"]
    if token: kwargs["access_token"] = flask.session["omnix.access_token"]
    try: data = quorum.get_json(url, **kwargs)
    except quorum.JsonError, error: handle_error(error)
    return data

def post_json(url, authenticate = True, token = False, **kwargs):
    if authenticate: kwargs["session_id"] = flask.session["omnix.session_id"]
    if token: kwargs["access_token"] = flask.session["omnix.access_token"]
    try: data = quorum.post_json(url, **kwargs)
    except quorum.JsonError, error: handle_error(error)
    return data

def put_json(url, authenticate = True, token = False, **kwargs):
    if authenticate: kwargs["session_id"] = flask.session["omnix.session_id"]
    if token: kwargs["access_token"] = flask.session["omnix.access_token"]
    try: data = quorum.put_json(url, **kwargs)
    except quorum.JsonError, error: handle_error(error)
    return data

def handle_error(error):
    data = error.get_data()
    exception = data.get("exception", {})
    exception_name = exception.get("exception_name", None)
    message = exception.get("message", None)
    if exception_name == "ControllerValidationReasonFailed":
        reset_session_id()
    elif exception_name:
        raise RuntimeError("%s - %s" % (exception_name, message))

def ensure_token():
    access_token = flask.session.get("omnix.access_token", None)
    if access_token: ensure_session_id(); return None

    url = config.BASE_URL + config.PREFIX + "oauth/authorize"
    values = {
        "client_id" : config.CLIENT_ID,
        "redirect_uri" : config.REDIRECT_URL,
        "response_type" : "code",
        "scope" : " ".join(config.SCOPE)
    }

    data = urllib.urlencode(values)
    url = url + "?" + data
    return url

def ensure_session_id():
    session_id = flask.session.get("omnix.session_id", None)
    if session_id: return None

    url = config.BASE_URL + "omni/oauth/start_session"
    contents_s = get_json(url, authenticate = False, token = True)
    username = contents_s.get("username", None)
    acl = contents_s.get("acl", None)
    session_id = contents_s.get("session_id", None)
    tokens = get_tokens(acl)

    flask.session["omnix.username"] = username
    flask.session["omnix.acl"] = acl
    flask.session["omnix.session_id"] = session_id
    flask.session["tokens"] = tokens
    flask.session["acl"] = quorum.check_login

def reset_session():
    if "omnix.access_token" in flask.session: del flask.session["omnix.access_token"]
    if "omnix.username" in flask.session: del flask.session["omnix.username"]
    if "omnix.acl" in flask.session: del flask.session["omnix.acl"]
    if "omnix.session_id" in flask.session: del flask.session["omnix.session_id"]
    if "tokens" in flask.session: del flask.session["tokens"]
    flask.session.modified = True

def reset_session_id():
    if "omnix.session_id" in flask.session:
        del flask.session["omnix.session_id"]
    if "omnix.access_token" in flask.session:
        del flask.session["omnix.access_token"]
    flask.session.modified = True
    ensure_session_id()

def get_tokens(acl):
    return acl.keys()
