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

import omni

from omnix.main import flask
from omnix.main import quorum
from omnix.util import config

def get_api(mode = omni.Api.OAUTH_MODE):
    access_token = flask.session and flask.session.get("omnix.access_token", None)
    session_id = flask.session and flask.session.get("omnix.session_id", None)
    api = omni.Api(
        base_url = config.OMNI_URL,
        prefix = config.PREFIX,
        client_id = config.CLIENT_ID,
        client_secret = config.CLIENT_SECRET,
        redirect_url = config.REDIRECT_URL,
        scope = config.SCOPE,
        access_token = access_token,
        session_id = session_id,
        username = config.USERNAME,
        password = config.PASSWORD,
        mode = mode
    )
    api.bind("auth", on_auth)
    return api

def ensure_api():
    access_token = flask.session.get("omnix.access_token", None)
    if access_token: return
    api = get_api()
    return api.oauth_authorize()

def on_auth(contents):
    start_session(contents)

def start_session(contents):
    if not flask.session: return

    username = contents.get("username", None)
    acl = contents.get("acl", None)
    session_id = contents.get("session_id", None)
    tokens = get_tokens(acl)

    flask.session["omnix.base_url"] = config.OMNI_URL
    flask.session["omnix.username"] = username
    flask.session["omnix.acl"] = acl
    flask.session["omnix.session_id"] = session_id
    flask.session["tokens"] = tokens

def reset_session():
    if not flask.session: return

    if "omnix.base_url" in flask.session: del flask.session["omnix.base_url"]
    if "omnix.access_token" in flask.session: del flask.session["omnix.access_token"]
    if "omnix.username" in flask.session: del flask.session["omnix.username"]
    if "omnix.acl" in flask.session: del flask.session["omnix.acl"]
    if "omnix.session_id" in flask.session: del flask.session["omnix.session_id"]
    if "tokens" in flask.session: del flask.session["tokens"]
    flask.session.modified = True

def get_tokens(acl):
    tokens = acl.keys()
    return quorum.legacy.eager(tokens)