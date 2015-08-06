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

import os
import imghdr
import shutil
import zipfile
import tempfile
import mimetypes

from omnix import util

from omnix.main import app
from omnix.main import flask
from omnix.main import quorum

@app.route("/extras", methods = ("GET",))
@quorum.ensure("base.user")
def list_extras():
    return flask.render_template(
        "extra/list.html.tpl",
        link = "extras"
    )

@app.route("/extras/media", methods = ("GET",))
@quorum.ensure("foundation.root_entity.set_media")
def media_extras():
    return flask.render_template(
        "extra/media.html.tpl",
        link = "extras"
    )

@app.route("/extras/media", methods = ("POST",))
@quorum.ensure("inventory.transactional_merchandise.update")
def do_media_extras():
    # retrieves the reference to the (omni) api object that
    # is going to be used for the operations of updating of
    # the merchandise in bulk (multiple operations at a time)
    api = util.get_api()

    # tries to retrieve the media file from the current
    # form in case it's not available renders the current
    # template with an error message
    media_file = quorum.get_field("media_file", None)
    if media_file == None or not media_file.filename:
        return flask.render_template(
            "extra/media.html.tpl",
            link = "extras",
            error = "No file defined"
        )

    # creates a temporary file path for the storage of the file
    # and then saves it into that directory, closing the same
    # file afterwards, as it has been properly saved
    fd, file_path = tempfile.mkstemp()
    try: media_file.save(file_path)
    finally: media_file.close()

    try:
        # creates a new temporary directory that is going to be used
        # in the extraction of the media zip file
        temp_path = tempfile.mkdtemp()
        try:
            # creates the zip file reference with the current file path
            # and then extracts the complete set of contents to the "target"
            # temporary path closing the zip file afterwards
            zip = zipfile.ZipFile(file_path)
            try: zip.extractall(temp_path)
            finally: zip.close()

            # iterates over the complete set of names in the temporary path
            # to try to upload the media to the target data source, note that
            # only the media files are considered and the base name of them
            # are going to be validation for existence in the data source
            for name in os.listdir(temp_path):
                # splits the file name into base name and extension and validates
                # the extension, so that only media files are considered
                base, extension = os.path.splitext(name)
                if not extension.lower() in (".png", ".jpg", ".jpeg"):
                    quorum.info("Skipping, '%s' not a valid media file" % name)
                    continue

                # splits the base value of the file name so that it's possible to
                # extract the proper position of the image if that's required
                base_s = base.rsplit("_", 1)
                if len(base_s) > 1: position = int(base_s[1])
                else: position = 1

                # tries to "cast" the base file name value as an integer and in case
                # it's possible assumes that this value is the object identifier
                try: object_id = int(base_s[0])
                except: object_id = None

                # in case no object id was retrieved from the base file name value
                # a secondary strategy is used, so that the merchandise database
                # is searched using the base string value as the company product code
                if not object_id:
                    # creates the keyword arguments map so that the the merchandise
                    # with the provided company product code is retrieved
                    kwargs = {
                        "start_record" : 0,
                        "number_records" : 1,
                        "filters[]" : [
                            "company_product_code:equals:%s" % base_s[0]
                        ]
                    }

                    # runs the list merchandise operation in order to try to find a
                    # merchandise entity for the requested (unique) product code in
                    # case there's at least one merchandise its object id is used
                    try: merchandise = api.list_merchandise(**kwargs)
                    except: merchandise = []
                    if merchandise: object_id = merchandise[0]["object_id"]

                # in case no object id was retrieved must skip the current loop
                # with a proper information message (as expected)
                if not object_id:
                    quorum.info("Skipping, could not resolve object id for '%s'" % base)
                    continue

                # prints a logging message about the upload of media file that
                # is going to be performed for the current entity
                quorum.debug(
                    "Adding media file for entity '%d' in position '%d'" %\
                    (object_id, position)
                )

                # creates the target temporary media path from the temporary directory
                # path and then "read" the complete set of contents from it closing the
                # file afterwards (no more reading allowed)
                media_path = os.path.join(temp_path, name)
                media_file = open(media_path, "rb")
                try: contents = media_file.read()
                finally: media_file.close()

                # tries to guess the proper image type for the image located at the
                # provided path and the uses this value to construct the mime type
                image_type = imghdr.what(media_path)
                mime_type = "image/" + image_type if image_type else "image/unknown"

                # sets/updates the media for the associated root entity using the
                # data extracted from the file and the information in its name
                api.set_media_entity(
                    object_id,
                    contents,
                    position = position,
                    mime_type = mime_type,
                    engine = "fs",
                    thumbnails = True
                )
        finally:
            # removes the temporary path as it's no longer going to be
            # required for the operation (errors are ignored)
            shutil.rmtree(temp_path, ignore_errors = True)
    finally:
        # closes the temporary file descriptor and removes the temporary
        # file (avoiding any memory leaks)
        os.close(fd)
        os.remove(file_path)

    # redirects the user back to the media list page with a success
    # message indicating that everything went as expected
    return flask.redirect(
        flask.url_for(
            "media_extras",
            message = "Media file processed with success"
        )
    )

@app.route("/extras/images", methods = ("GET",))
@quorum.ensure("inventory.transactional_merchandise.update")
def images_extras():
    return flask.render_template(
        "extra/images.html.tpl",
        link = "extras"
    )

@app.route("/extras/images", methods = ("POST",))
@quorum.ensure("inventory.transactional_merchandise.update")
def do_images_extras():
    # retrieves the reference to the (omni) api object that
    # is going to be used for the operations of updating of
    # the merchandise in bulk (multiple operations at a time)
    api = util.get_api()

    # tries to retrieve the images file from the current
    # form in case it's not available renders the current
    # template with an error message
    images_file = quorum.get_field("images_file", None)
    if images_file == None or not images_file.filename:
        return flask.render_template(
            "extra/images.html.tpl",
            link = "extras",
            error = "No file defined"
        )

    # creates a temporary file path for the storage of the file
    # and then saves it into that directory, closing the same
    # file afterwards, as it has been properly saved
    fd, file_path = tempfile.mkstemp()
    try: images_file.save(file_path)
    finally: images_file.close()

    try:
        # creates a new temporary directory that is going to be used
        # in the extraction of the images zip file
        temp_path = tempfile.mkdtemp()
        try:
            # creates the zip file reference with the current file path
            # and then extracts the complete set of contents to the "target"
            # temporary path closing the zip file afterwards
            zip = zipfile.ZipFile(file_path)
            try: zip.extractall(temp_path)
            finally: zip.close()

            # iterates over the complete set of names in the temporary path
            # to try to upload the image to the target data source, note that
            # only the image files are considered and the base name of them
            # are going to be validation for existence in the data source
            for name in os.listdir(temp_path):
                # splits the file name into base name and extension and validates
                # the extension, so that only image files are considered
                base, extension = os.path.splitext(name)
                if not extension.lower() in (".png", ".jpg", ".jpeg"):
                    quorum.info("Skipping, '%s' not a valid image file" % name)
                    continue

                # creates the keyword arguments map so that the the merchandise
                # with the provided company product code is retrieved
                kwargs = {
                    "start_record" : 0,
                    "number_records" : 1,
                    "filters[]" : [
                        "company_product_code:equals:%s" % base
                    ]
                }

                # creates the url for the merchandise retrieval and runs the get
                # operation with the provided filter so that the target merchandise
                # is retrieved for object id validation
                merchandise = api.list_merchandise(**kwargs)

                # verifies that at least one entity was retrieved in case nothing
                # is found skips the current loop with a not found error
                if not merchandise:
                    quorum.info("Skipping, '%s' not found in data source" % base)
                    continue

                # prints a logging message about the upload of image file that
                # is going to be performed for the current merchandise
                quorum.debug("Changing image file for merchandise '%s'" % base)

                # retrieves the first entity from the resulting list and then retrieves
                # the object identifier from it to be used in the update operation
                entity = merchandise[0]
                object_id = entity["object_id"]

                # creates the target temporary image path from the temporary directory
                # path and then "read" the complete set of contents from it closing the
                # file afterwards (no more reading allowed)
                image_path = os.path.join(temp_path, name)
                image_file = open(image_path, "rb")
                try: contents = image_file.read()
                finally: image_file.close()

                # creates the image (file) tuple with both the name of the file and the
                # contents if it (multipart standard)
                image_tuple = (name, contents)

                # creates the multipart data map with both the object id and the image
                # file parameters that are going to be used in the encoding
                data_m = {
                    "object_id" : object_id,
                    "transactional_merchandise[_parameters][image_file]" : image_tuple
                }

                # uses the "resolved" items structure in the operation to
                # the omni api so that the images for them get updated
                api.update_merchandise(object_id, data_m)
        finally:
            # removes the temporary path as it's no longer going to be
            # required for the operation (errors are ignored)
            shutil.rmtree(temp_path, ignore_errors = True)
    finally:
        # closes the temporary file descriptor and removes the temporary
        # file (avoiding any memory leaks)
        os.close(fd)
        os.remove(file_path)

    # redirects the user back to the images list page with a success
    # message indicating that everything went as expected
    return flask.redirect(
        flask.url_for(
            "images_extras",
            message = "Images file processed with success"
        )
    )

@app.route("/extras/prices", methods = ("GET",))
@quorum.ensure("inventory.transactional_merchandise.update")
def prices_extras():
    return flask.render_template(
        "extra/prices.html.tpl",
        link = "extras"
    )

@app.route("/extras/prices", methods = ("POST",))
@quorum.ensure("inventory.transactional_merchandise.update")
def do_prices_extras():
    # retrieves the reference to the api object that is going
    # to be used for the updating of prices operation
    api = util.get_api()

    # tries to retrieve the prices file from the current
    # form in case it's not available renders the current
    # template with an error message
    prices_file = quorum.get_field("prices_file", None)
    if prices_file == None or not prices_file.filename:
        return flask.render_template(
            "extra/prices.html.tpl",
            link = "extras",
            error = "No file defined"
        )

    # creates a temporary file path for the storage of the file
    # and then saves it into that directory
    fd, file_path = tempfile.mkstemp()
    prices_file.save(file_path)

    try:
        # parses the temporary file containing the spreadsheet according
        # to the provided set of keys (to create the correct structures)
        items = quorum.xlsx_to_map(
            file_path,
            keys = ("company_product_code", "retail_price")
        )
    finally:
        # closes the temporary file descriptor and removes the temporary
        # file (avoiding any memory leaks)
        os.close(fd)
        os.remove(file_path)

    # uses the "resolved" items structure in the put operation to
    # the omni api so that the prices for them get updated
    api.prices_merchandise(items)

    # redirects the user back to the prices list page with a success
    # message indicating that everything went ok
    return flask.redirect(
        flask.url_for(
            "prices_extras",
            message = "Prices file processed with success"
        )
    )

@app.route("/extras/ctt", methods = ("GET",))
@quorum.ensure("sales.sale_order.list")
def ctt_extras():
    return flask.render_template(
        "extra/ctt.html.tpl",
        link = "extras"
    )

@app.route("/extras/ctt", methods = ("POST",))
@quorum.ensure("sales.sale_order.list")
def do_ctt_extras():
    api = util.get_api()
    sale_orders = api.list_sale_orders(**{
        "start_record" : 0,
        "number_records" : -1,
        "eager[]" : [
            "customer",
            "customer.primary_contact_information",
            "shipping_address"
        ],
        "filters[]" : [
            "workflow_state:equals:5",
            "shipping_type:equals:2"
        ]
    })

    out_data = util.encode_ctt(sale_orders, encoding = "Cp1252")

    return flask.Response(
        out_data,
        mimetype = "binary/octet-stream"
    )

@app.route("/extras/template", methods = ("GET",))
@quorum.ensure("base.user")
def template_extras():
    return flask.render_template(
        "extra/template.html.tpl",
        link = "extras"
    )

@app.route("/extras/template", methods = ("POST",))
@quorum.ensure("foundation.system_company.show.self")
def do_template_extras():
    object = quorum.get_object()
    mask_name = object.get("mask_name", None)
    format = object.get("format", "png")
    base_file = object.get("base_file", None)
    base_data = base_file.read()

    mask_name = "mask_" + mask_name if mask_name else "mask"
    mask_name = mask_name.lower()
    mask_name = mask_name.replace(" ", "_")

    api = util.get_api()
    try: mask_data = api.public_media_system_company(label = mask_name)
    except: mask_data = None
    if not mask_data: raise quorum.OperationalError("No mask defined")

    out_data = util.mask_image(base_data, mask_data, format = format)
    mimetype = mimetypes.guess_type("_." + format)[0]

    return flask.Response(
        out_data,
        mimetype = mimetype or "application/octet-stream"
    )

@app.route("/extras/mask", methods = ("POST",))
@quorum.ensure("foundation.root_entity.set_media")
def do_mask_extras():
    object = quorum.get_object()
    mask_name = object.get("mask_name", None)
    mask_file = object.get("mask_file", None)

    mask_name = "mask_" + mask_name if mask_name else "mask"
    mask_name = mask_name.lower()
    mask_name = mask_name.replace(" ", "_")

    api = util.get_api()
    system_company = api.self_system_company()

    data = mask_file.read()
    mime_type = mask_file.content_type
    api.set_media_entity(
        system_company["object_id"],
        mask_name,
        data = data,
        mime_type = mime_type,
        visibility = 2
    )

    return flask.redirect(
        flask.url_for(
            "template_extras",
            message = "Mask file uploaded with success"
        )
    )

@app.route("/extras/browser", methods = ("GET",))
@quorum.ensure("foundation.root_entity.show_media")
def browser_extras():
    return flask.render_template(
        "extra/browser.html.tpl",
        link = "extras"
    )

@app.route("/extras/browser", methods = ("POST",), json = True)
@quorum.ensure("foundation.root_entity.show_media")
def do_browser():
    object_id = quorum.get_field("object_id", None, cast = int)
    api = util.get_api()
    entity = api.get_entity(object_id)
    media = api.info_media_entity(object_id)
    media_info = []
    for item in media:
        mitem = dict(
            object_id = item["object_id"],
            label = item["label"],
            position = item["position"],
            dimensions = item["dimensions"],
            image_url = api.get_media_url(item["secret"])
        )
        media_info.append(mitem)
    media_info.sort(key = _media_sorter)
    entity["media"] = media_info
    return entity

@app.route("/extras/browser/new_media/<int:id>", methods = ("GET",))
@quorum.ensure("foundation.root_entity.set_media")
def new_media_browser(id):
    return flask.render_template(
        "extra/browser/new_media.html.tpl",
        link = "extras",
        object_id = id,
        media = dict(),
        errors = dict()
    )

@app.route("/extras/browser/new_media/<int:id>", methods = ("POST",))
@quorum.ensure("foundation.root_entity.set_media")
def create_media_browser(id):
    api = util.get_api()
    engine = quorum.get_field("engine", None) or None
    position = quorum.get_field("position", None, cast = int)
    label = quorum.get_field("label", None) or None
    visibility = quorum.get_field("visibility", None, cast = int)
    description = quorum.get_field("description", None) or None
    thumbnails = quorum.get_field("thumbnails", False, cast = bool)
    media_file = quorum.get_field("media_file", None)
    image_type = mimetypes.guess_type(media_file.filename)[0]
    mime_type = image_type if image_type else "image/unknown"
    try: data = media_file.stream.read()
    finally: media_file.close()
    media = api.set_media_entity(
        id,
        data,
        engine = engine,
        position = position,
        label = label,
        mime_type = mime_type,
        visibility = visibility,
        description = description,
        thumbnails = thumbnails
    )
    return flask.redirect(
        flask.url_for("media_browser", id = media["object_id"])
    )

@app.route("/extras/browser/media/<int:id>", methods = ("GET",))
@quorum.ensure("foundation.media.show")
def media_browser(id):
    api = util.get_api()
    media = api.info_media(id)
    media["image_url"] = api.get_media_url(media["secret"])
    return flask.render_template(
        "extra/browser/media.html.tpl",
        link = "extras",
        sub_link = "info",
        media = media
    )

@app.route("/extras/browser/media/<int:id>/edit", methods = ("GET",))
@quorum.ensure("foundation.media.update")
def edit_media_browser(id):
    api = util.get_api()
    media = api.info_media(id)
    return flask.render_template(
        "extra/browser/edit_media.html.tpl",
        link = "extras",
        sub_link = "edit",
        media = media,
        errors = dict()
    )

@app.route("/extras/browser/media/<int:id>/update", methods = ("POST",))
@quorum.ensure("foundation.media.update")
def update_media_browser(id):
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
        flask.url_for("media_browser", id = media["object_id"])
    )

@app.route("/extras/browser/media/<int:id>/delete", methods = ("GET",))
@quorum.ensure("foundation.media.delete")
def delete_media_browser(id):
    api = util.get_api()
    api.delete_media(id)
    return flask.redirect(
        flask.url_for("browser_extras")
    )

def _media_sorter(item):
    return (
        item["label"] or "",
        item["position"] or 0,
        item["dimensions"] or ""
    )
