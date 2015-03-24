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

def encode_ctt(sale_orders, encoding = None):
    lines = []

    for sale_order in sale_orders:
        line = dict(
            reference = sale_order["extended_identifier"][:21],
            quantity = 1,
            weight = "100,00gr",
            price = "0ue",
            name = sale_order["customer"]["representation"][:60],
            address = sale_order["shipping_address"]["street_name"][:60],
            town = sale_order["shipping_address"]["zip_code_name"][:50],
            zip_code_4 = sale_order["shipping_address"]["zip_code"].split("-", 1)[0][:4],
            zip_code_3 = sale_order["shipping_address"]["zip_code"].split("-", 1)[1][:3],
            not_applicable_1 = "",
            observations = "",
            back = 0,
            document_code = "",
            phone_number = (sale_order["customer"]["primary_contact_information"]["phone_number"] or "")[:15],
            saturday = 1,
            email = (sale_order["customer"]["primary_contact_information"]["email"] or "")[:200],
            country = "PT",
            fragile = 0,
            not_applicable_2 = "",
            document_collection = "",
            code_email = "",
            mobile_phone = (sale_order["customer"]["primary_contact_information"]["mobile_phone_number"] or "")[:15],
            second_delivery = 0,
            delivery_date = "",
            return_signed_document = 0,
            expeditor_instructions = 0,
            sms = 1,
            not_applicable_3 = "",
            printer = "",
            ticket_machine = "",
            at_code = ""
        )

        line = "+".join([
            line["reference"],
            str(line["quantity"]),
            line["weight"],
            line["price"],
            line["name"],
            line["address"],
            line["town"],
            line["zip_code_4"],
            line["zip_code_3"],
            line["not_applicable_1"],
            line["observations"],
            str(line["back"]),
            line["document_code"],
            line["phone_number"],
            str(line["saturday"]),
            line["email"],
            line["country"],
            str(line["fragile"]),
            line["not_applicable_2"],
            line["document_collection"],
            line["code_email"],
            line["mobile_phone"],
            str(line["second_delivery"]),
            line["delivery_date"],
            str(line["return_signed_document"]),
            str(line["expeditor_instructions"]),
            str(line["sms"]),
            line["not_applicable_3"],
            line["printer"],
            line["ticket_machine"],
            line["at_code"]
        ])

        lines.append(line)

    ctt_data = "\n".join(lines)
    if encoding: ctt_data = ctt_data.encode(encoding)

    return ctt_data