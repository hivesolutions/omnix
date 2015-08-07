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

from omnix import util

from omnix.main import app
from omnix.main import flask
from omnix.main import quorum

@app.route("/entities", methods = ("GET",))
@quorum.ensure("foundation.root_entity.list")
def list_entities():
    return flask.render_template(
        "entity/list.html.tpl",
        link = "entities"
    )

@app.route("/entities.json", methods = ("GET",), json = True)
@quorum.ensure("foundation.root_entity.list")
def list_entities_json():
    api = util.get_api()
    object = quorum.get_object()
    return api.list_entities(**object)

@app.route("/entities/<int:id>", methods = ("GET",))
@quorum.ensure("foundation.root_entity.show")
def show_entities(id):
    api = util.get_api()
    entity = api.get_entity(id)
    return flask.render_template(
        "entity/show.html.tpl",
        link = "entities",
        sub_link = "info",
        entity = entity
    )

@app.route("/entities/<int:id>/edit", methods = ("GET",))
@quorum.ensure("foundation.root_entity.update")
def edit_entities(id):
    api = util.get_api()
    entity = api.get_entity(id)
    return flask.render_template(
        "entity/edit.html.tpl",
        link = "entities",
        sub_link = "edit",
        entity = entity,
        errors = dict()
    )

@app.route("/entities/<int:id>/update", methods = ("POST",))
@quorum.ensure("foundation.root_entity.update")
def update_entities(id):
    return flask.redirect(
        flask.url_for("show_entity", id = entity["object_id"])
    )
