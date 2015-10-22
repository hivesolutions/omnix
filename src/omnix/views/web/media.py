#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Omnix System
# Copyright (c) 2008-2015 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import mimetypes

from omnix import util

from omnix.main import app
from omnix.main import flask
from omnix.main import quorum

@app.route("/media", methods = ("GET",))
@quorum.ensure("foundation.media.list")
def list_media():
    return flask.render_template(
        "media/list.html.tpl",
        link = "media"
    )

@app.route("/media.json", methods = ("GET",), json = True)
@quorum.ensure("foundation.media.list")
def list_media_json():
    api = util.get_api()
    object = quorum.get_object()
    return api.list_media(**object)

@app.route("/media/<int:id>", methods = ("GET",))
@quorum.ensure("foundation.media.show")
def show_media(id):
    api = util.get_api()
    media = api.info_media(id)
    media["image_url"] = api.get_media_url(media["secret"])
    return flask.render_template(
        "media/show.html.tpl",
        link = "media",
        sub_link = "info",
        media = media
    )

@app.route("/media/<int:id>/edit", methods = ("GET",))
@quorum.ensure("foundation.media.update")
def edit_media(id):
    api = util.get_api()
    media = api.info_media(id)
    return flask.render_template(
        "media/edit.html.tpl",
        link = "media",
        sub_link = "edit",
        media = media,
        errors = dict()
    )

@app.route("/media/<int:id>/update", methods = ("POST",))
@quorum.ensure("foundation.media.update")
def update_media(id):
    api = util.get_api()
    position = quorum.get_field("position", None, cast = int)
    label = quorum.get_field("label", None) or None
    visibility = quorum.get_field("visibility", None, cast = int)
    description = quorum.get_field("description", None) or None
    media_file = quorum.get_field("media_file", None)
    image_type = mimetypes.guess_type(media_file.filename)[0]
    mime_type = image_type if image_type else "image/unknown"
    media = dict(
        position = position,
        label = label,
        visibility = visibility,
        description = description
    )
    payload = dict(media = media)
    if media_file:
        try: data = media_file.stream.read()
        finally: media_file.close()
        media["mime_type"] = mime_type
        payload["data"] = data
    media = api.update_media(id, payload)
    return flask.redirect(
        flask.url_for("show_media", id = media["object_id"])
    )

@app.route("/media/<int:id>/delete", methods = ("GET",))
@quorum.ensure("foundation.media.delete")
def delete_media(id):
    api = util.get_api()
    api.delete_media(id)
    return flask.redirect(
        flask.url_for("list_media")
    )