#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Omnix System
# Copyright (C) 2008-2015 Hive Solutions Lda.
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

import quorum

LOCAL_PREFIX = "omni_adm/"
""" The web prefix to be used when trying to access administration
related resources from a local perspective """

REMOTE_PREFIX = "adm/"
""" The web prefix to be used when trying to access administration
related resources from a remote perspective """

LOCAL_URL = "http://localhost:8080/mvc/"
""" The base url to be used to compose the various
complete url values for the various operations, this is
the local version of it used mostly for debugging """

REMOTE_URL = "https://ldj.frontdoorhd.com/"
""" The base url to be used to compose the various
complete url values for the various operations, this is
the remove version used in production environments """

REDIRECT_URL = "http://localhost:8181/oauth"
""" The redirect base url to be used as the base value
for the construction of the base url instances """

CLIENT_ID = "cabf02130bbe4886984ebfcfad9ec9e5"
""" The id of the omni client to be used, this value
is not considered to be secret and may be freely used """

CLIENT_SECRET = "4c37a7dff4c3411ba1646093d2109d87"
""" The secret key value to be used to access the
omni api as the client, this value should not be shared
with every single person (keep private) """

FIRST_DAY = 1
""" The constant value that defines the first day of a month
this is obvious and should be used as a constant for readability """

SCOPE = (
    "base",
    "base.user",
    "base.admin",
    "foundation.store.list",
    "foundation.store.show",
    "foundation.employee.list",
    "foundation.employee.show",
    "foundation.employee.show.self",
    "foundation.root_entity.show_media",
    "foundation.root_entity.set_media",
    "foundation.supplier_company.list",
    "foundation.supplier_company.show",
    "foundation.system_company.show.self",
    "customers.customer_person.list",
    "customers.customer_person.show",
    "sales.customer_return.list",
    "sales.customer_return.list.self",
    "sales.sale_transaction.list",
    "sales.sale_transaction.list.self",
    "documents.signed_document.list",
    "documents.signed_document.submit_invoice_at",
    "analytics.sale_snapshot.list",
    "analytics.employee_snapshot.list",
    "inventory.transactional_merchandise.list",
    "inventory.transactional_merchandise.update"
)
""" The list of permissions to be used to create the
scope string for the oauth value """

AT_SALE_TYPES = (
    "MoneySaleSlip",
    "Invoice",
    "CreditNote",
    "DebitNote"
)
""" The list containing the complete set of types that
are considered to be of type sake """

AT_TRANSPORT_TYPES = (
    "TransportationSlip",
    "ExpeditionSlip"
)
""" The list containing the complete set of types that
are considered to be of type transport """

AT_SUBMIT_TYPES = AT_SALE_TYPES + AT_TRANSPORT_TYPES
""" The set of valid types for submission to at, note
that this range of values should be changed with care """

REMOTE = quorum.conf("REMOTE", False)
BASE_URL = quorum.conf("BASE_URL", "http://localhost:8181")
REDIRECT_URL = quorum.conf("REDIRECT_URL", REDIRECT_URL)
SENDER_EMAIL = quorum.conf("SENDER_EMAIL", "Omnix <no-reply@omnix.com>")
USERNAME = quorum.conf("OMNIX_USERNAME", None)
PASSWORD = quorum.conf("OMNIX_PASSWORD", None)
SCHEDULE = quorum.conf("OMNIX_SCHEDULE", True, cast = bool)
COMMISSION_RATE = quorum.conf("OMNIX_COMMISSION_RATE", 0.01, cast = float)
COMMISSION_DAY = quorum.conf("OMNIX_COMMISSION_DAY", 26, cast = int)

OMNI_URL = REMOTE_URL if REMOTE else LOCAL_URL
PREFIX = REMOTE_PREFIX if REMOTE else LOCAL_PREFIX
