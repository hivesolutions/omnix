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

import csv

import quorum

def csv_file(
    file,
    callback,
    header = False,
    delimiter = ",",
    strict = False
):
    _file_name, mime_type, data = file
    is_csv = mime_type in ("text/csv", "application/vnd.ms-excel")
    if not is_csv and strict:
        raise quorum.OperationalError("Invalid mime type '%s'" % mime_type)
    data = data.decode("utf-8")
    buffer = quorum.legacy.StringIO(data)
    return csv_import(
        buffer,
        callback,
        header = header,
        delimiter = delimiter
    )

def csv_import(buffer, callback, header = False, delimiter = ","):
    csv_reader = csv.reader(
        buffer,
        delimiter = delimiter,
        quoting = csv.QUOTE_NONE
    )
    if header: _header = next(csv_reader)
    for line in csv_reader: callback(line)
