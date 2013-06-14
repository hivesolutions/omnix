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
import json
import tempfile

import util

from omnix import app
from omnix import flask
from omnix import quorum

@app.route("/extras", methods = ("GET",))
def list_extras():
    return flask.render_template(
        "extra/list.html.tpl",
        link = "extras"
    )

@app.route("/extras/prices", methods = ("GET",))
def prices_extras():
    return flask.render_template(
        "extra/prices.html.tpl",
        link = "extras"
    )

def xls_to_map(file_path, keys = (), ignore_header = True):
    import xlrd

    # creates the list structure that is going to store the
    # complete set of parsed items according to the provided
    # keys list specification
    items = []

    # opens the workbook in the provided file path for reading
    # of its contents and construction of the final structure
    workbook = xlrd.open_workbook(file_path)

    # retrieves the list of sheets in the document and retrieves
    # the first of its sheets, this the one that is going to be
    # used in the processing of the contents (considered primary)
    sheets = workbook.sheets()
    sheet = sheets[0]

    # iterates over the complete set of valid rows in the sheet
    # to process its contents, the valid rows are the ones that
    # contain any sort of data
    for row in range(sheet.nrows):
        # in case the ignore header flag is set and the current
        # row index is zero must continue the loop ignoring it
        if row == 0 and ignore_header: continue

        # creates the map that is going to be used in the construction
        # of the item elements and then iterates over all the expected
        # key values to populate it
        item = {}
        cell = 0
        for key in keys:
            cell_s = sheet.cell(row, cell)
            value = cell_s.value
            item[key] = value
            cell += 1

        # adds the item map that has been constructed to the list of
        # parsed items for the current spreadsheet
        items.append(item)

    # returns the final list of map items resulting from the parsing
    # of the spreadsheet file containing key to value assignments
    return items

@app.route("/extras/prices", methods = ("POST",))
def do_prices_extras():
    url = util.ensure_token()
    if url: return flask.redirect(url)

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

    # parses the temporary file containing the spreadsheet according
    # to the provided set of keys and then closes the temporary file
    # descriptor and remove the temporary file (avoids leaks)
    try: items = xls_to_map(file_path, keys = ("company_product_code", "retail_price"))
    finally: os.close(fd); os.remove(file_path)

    # uses the "resolved" items structure in the put operation to
    # the omni api so that the prices for them get updated
    url = util.BASE_URL + "omni/merchandise/prices.json"
    util.put_json(
        url,
        data = json.dumps(items),
        mime = "application/json"
    )

    # redirects the user back to the prices list page with a success
    # message indicating that everything went ok
    return flask.redirect(
        flask.url_for(
            "prices_extras",
            message = "Prices file processed with success"
        )
    )
