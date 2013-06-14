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

DEBUG = True
""" The flag that controls if the current execution is meant
to be used for debugging purposes (locally) """

LOCAL_PREFIX = "omni_web_adm/"
""" The web prefix to be used when trying to access administration
related resources from a local perspective """

REMOTE_PREFIX = "adm/"
""" The web prefix to be used when trying to access administration
related resources from a remote perspective """

LOCAL_URL = "http://localhost:8080/dynamic/rest/mvc/"
""" The base url to be used to compose the various
complete url values for the various operations, this is
the local version of it used mostly for debugging """

REMOTE_URL = "https://erp.startomni.com/"
""" The base url to be used to compose the various
complete url values for the various operations, this is
the remove version used in production environments """

REDIRECT_URL = "http://localhost:8181/oauth"
""" The redirect base url to be used as the base value
for the construction of the base url instances """

CLIENT_ID = "cabf02130bbe4886984ebfcfad9ec9e5"
""" The id of the omni client to be used """

CLIENT_SECRET = "4c37a7dff4c3411ba1646093d2109d87"
""" The secret key value to be used to access the
omni api as the client """

SCOPE = (
    "foundation.store.list",
    "foundation.store.show",
    "foundation.employee.list",
    "foundation.employee.show",
    "foundation.supplier_company.list",
    "foundation.supplier_company.show",
    "customers.customer_person.list",
    "customers.customer_person.show",
    "documents.signed_document.list",
    "documents.signed_document.submit_at",
    "analytics.sale_snapshot.list"
)
""" The list of permission to be used to create the
scope string for the oauth value """

AT_SUBMIT_TYPES = (
    "MoneySaleSlip",
    "Invoice",
    "CreditNote",
    "DebitNote"
)
""" The set of valid types for submission to at """

BASE_URL = LOCAL_URL if DEBUG else REMOTE_URL
PREFIX = LOCAL_PREFIX if DEBUG else REMOTE_PREFIX