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

@app.route("/", methods = ("GET",))
@app.route("/index", methods = ("GET",))
@quorum.ensure("foundation.oauth.start_session")
def index():
    return flask.render_template(
        "index.html.tpl",
        link = "home"
    )

@app.route("/signin", methods = ("GET",))
def signin():
    return flask.render_template(
        "signin.html.tpl"
    )

@app.route("/signin", methods = ("POST",))
def login():
    url = util.ensure_token()
    if url: return flask.redirect(url)
    return flask.redirect(
        flask.url_for("index")
    )

@app.route("/signin_do", methods = ("GET",))
def do_login():
    url = util.ensure_token()
    if url: return flask.redirect(url)
    return flask.redirect(
        flask.url_for("index")
    )

@app.route("/logout", methods = ("GET",))
def logout():
    util.reset_session()
    return flask.redirect(
        flask.url_for("index")
    )

@app.route("/about", methods = ("GET",))
@quorum.ensure("foundation.oauth.start_session")
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
    util.reset_session()

    return flask.redirect(
        flask.url_for("index")
    )

@app.route("/flush_at", methods = ("GET",))
def flush_at():
    url = util.ensure_token()
    if url: return flask.redirect(url)

    # creates a values map structure to retrieve the complete
    # set of inbound documents that have not yet been submitted
    # to at for the flush operation
    kwargs = {
        "filter_string" : "",
        "start_record" : 0,
        "number_records" : 1000,
        "sort" : "issue_date:ascending",
        "filters[]" : [
            "issue_date:greater:1356998400",
            "submitted_at:equals:2",
            "document_type:equals:3"
        ]
    }
    url = util.BASE_URL + "omni/signed_documents.json"
    contents_s = util.get_json(url, **kwargs)

    # filters the result set retrieved so that only the valid at
    # "submittable" documents are present in the sequence
    valid_documents = [value for value in contents_s\
        if value["_class"] in util.AT_SUBMIT_TYPES]

    # "calculates" the total set of valid documents present in the
    # valid documents and starts the index counter
    total = len(valid_documents)
    index = 1

    # iterates over the complete set of valid documents to be sent
    # (submitted) to at and processes the submission
    for document in valid_documents:
        type = document["_class"]
        object_id = document["object_id"]
        representation = document["representation"]
        issue_date = document["issue_date"]
        issue_date_d = datetime.datetime.utcfromtimestamp(issue_date)
        issue_date_s = issue_date_d.strftime("%d %b %Y %H:%M:%S")

        # retrieves the current time and uses it to print debug information
        # about the current document submission to at
        quorum.info(
            "Submitting %s - %s (%s) [%d/%d]" % (
                type,
                representation,
                issue_date_s,
                index,
                total
            )
        )

        try:
            # creates the complete url value for the submission
            # operation and run the submission for the current document
            url = util.BASE_URL + "omni/signed_documents/submit_invoice_at.json"
            util.get_json(url, document_id = object_id)
        except BaseException, exception:
            quorum.error("Exception while submitting document - %s" % unicode(exception))
        else:
            quorum.info("Document submitted with success")

        # increments the index counter, because one more document
        # as been processed (submitted or failed)
        index += 1

    return flask.render_template(
        "index.html.tpl",
        link = "home"
    )

@app.route("/oauth", methods = ("GET",))
def oauth():
    # retrieves the code value provided that is going to be used
    # to redeem the access token
    code = quorum.get_field("code", None)

    # tries to retrieve the error field an in case it exists raises
    # an error indicating the oauth based problem
    error = quorum.get_field("error", None)
    error_description = quorum.get_field("error_description", None)
    if error: raise RuntimeError("%s - %s" % (error, error_description))

    # creates the access token url for the api usage and sends the
    # appropriate attributes for the retrieval of the access token,
    # then stores it in the current session
    url = util.BASE_URL + "omni/oauth/access_token"
    contents_s = util.post_json(
        url,
        authenticate = False,
        token = False,
        client_id = util.CLIENT_ID,
        client_secret = util.CLIENT_SECRET,
        grant_type = "authorization_code",
        redirect_uri = util.REDIRECT_URL,
        code = code
    )
    access_token = contents_s["access_token"]
    flask.session["omnix.access_token"] = access_token

    # ensures that a correct session id value exists in session, creating
    # a new session in case that's required
    util.ensure_session_id()

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

@app.errorhandler(404)
def handler_404(error):
    return str(error)

@app.errorhandler(413)
def handler_413(error):
    return str(error)

@app.errorhandler(BaseException)
def handler_exception(error):
    return str(error)
