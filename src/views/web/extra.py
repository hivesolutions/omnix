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

import os
import shutil
import zipfile
import tempfile

import util

from omnix import app
from omnix import flask
from omnix import quorum

@app.route("/extras", methods = ("GET",))
@quorum.ensure("base.admin")
def list_extras():
    return flask.render_template(
        "extra/list.html.tpl",
        link = "extras"
    )

@app.route("/extras/images", methods = ("GET",))
@quorum.ensure("base.admin")
def images_extras():
    return flask.render_template(
        "extra/images.html.tpl",
        link = "extras"
    )

@app.route("/extras/images", methods = ("POST",))
@quorum.ensure("base.admin")
def do_images_extras():
    url = util.ensure_token()
    if url: return flask.redirect(url)

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
    # and then saves it into that directory
    fd, file_path = tempfile.mkstemp()
    images_file.save(file_path)

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
                if not extension in (".png",):
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
                url = util.BASE_URL + "omni/merchandise.json"
                contents_s = util.get_json(
                    url,
                    **kwargs
                )

                # verifies that at least one entity was retrieved in case nothing
                # is found skips the current loop with a not found error
                if not contents_s:
                    quorum.info("Skipping, '%s' not found in data source" % base)
                    continue

                # retrieves the first entity from the resulting list and then retrieves
                # the object identifier from it to be used in the update operation
                entity = contents_s[0]
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

                # uses the "resolved" items structure in the post operation to
                # the omni api so that the images for them get updated
                url = util.BASE_URL + "omni/merchandise/%d/update.json" % object_id
                util.post_json(url, data_m = data_m)
        finally:
            # removes the temporary path as it's no longer going to be
            # required for the operation (errors are ignored)
            shutil.rmtree(temp_path, ignore_errors = True)
    finally:
        # closes the temporary file descriptor and removes the temporary
        # file (avoiding any memory leaks)
        os.close(fd);
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
@quorum.ensure("base.admin")
def prices_extras():
    return flask.render_template(
        "extra/prices.html.tpl",
        link = "extras"
    )

@app.route("/extras/prices", methods = ("POST",))
@quorum.ensure("base.admin")
def do_prices_extras():
    url = util.ensure_token()
    if url: return flask.redirect(url)

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
        os.close(fd);
        os.remove(file_path)

    # uses the "resolved" items structure in the put operation to
    # the omni api so that the prices for them get updated
    url = util.BASE_URL + "omni/merchandise/prices.json"
    util.put_json(url, data_j = items)

    # redirects the user back to the prices list page with a success
    # message indicating that everything went ok
    return flask.redirect(
        flask.url_for(
            "prices_extras",
            message = "Prices file processed with success"
        )
    )
