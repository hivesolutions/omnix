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

import calendar
import datetime

import quorum

from . import logic
from . import config

BIRTHDAY_SUBJECT = dict(
    en_us = "Happy Birthday",
    pt_pt = "Feliz Aniversário"
)

ACTIVITY_SUBJECT = dict(
    en_us = "Omni activity report for %s as of %s",
    pt_pt = "Relatório de atividade Omni para %s em %s"
)

def mail_birthday_all(
    api = None,
    month = None,
    day = None,
    validate = False,
    links = True
):
    api = api or logic.get_api()
    has_date = month and day
    if not has_date:
        current = datetime.datetime.utcnow()
        month, day = current.month, current.day
    birth_day = "%02d/%02d" % (month, day)
    employees = api.list_employees(
        object = dict(limit = -1),
        **{
            "filters[]" : [
                "birth_day:equals:%s" % birth_day
            ]
        }
    )
    for employee in employees:
        try: mail_birthday(
            api = api,
            id = employee["object_id"],
            links = links
        )
        except quorum.OperationalError: pass

def mail_activity_all(
    api = None,
    year = None,
    month = None,
    validate = False,
    links = True
):
    api = api or logic.get_api()
    employees = api.list_employees(object = dict(limit = -1))
    for employee in employees:
        try: mail_activity(
            api = api,
            id = employee["object_id"],
            year = year,
            month = month,
            validate = validate,
            links = links
        )
        except quorum.OperationalError: pass

def mail_birthday(api = None, id = None, links = True):
    api = api or logic.get_api()
    employee = api.get_employee(id) if id else api.self_employee()

    name = employee.get("full_name", None)
    working = employee.get("working", None)
    contact_information = employee.get("primary_contact_information", {})
    email = contact_information.get("email", None)

    if not name: raise quorum.OperationalError("No name defined")
    if not email: raise quorum.OperationalError("No email defined")
    if not working == 1: raise quorum.OperationalError("No longer working")

    quorum.debug("Sending birthday email to %s <%s>" % (name, email))
    quorum.send_mail(
        subject = BIRTHDAY_SUBJECT[config.LOCALE],
        sender = config.SENDER_EMAIL,
        receivers = ["%s <%s>" % (name, email)],
        rich = "email/birthday.%s.html.tpl" % config.LOCALE,
        context = dict(
            settings = dict(
                logo = True,
                links = links
            ),
            base_url = config.BASE_URL,
            omnix_base_url = config.OMNI_URL,
            commission_rate = config.COMMISSION_RATE
        )
    )

def mail_activity(
    api = None,
    id = None,
    year = None,
    month = None,
    validate = False,
    links = True
):
    api = api or logic.get_api()
    employee = api.get_employee(id) if id else api.self_employee()

    name = employee.get("full_name", None)
    working = employee.get("working", None)
    contact_information = employee.get("primary_contact_information", {})
    email = contact_information.get("email", None)

    if not name: raise quorum.OperationalError("No name defined")
    if not email: raise quorum.OperationalError("No email defined")
    if not working == 1: raise quorum.OperationalError("No longer working")

    now = datetime.datetime.utcnow()
    now_s = now.strftime("%B %d %Y")

    operations,\
    target_s,\
    sales_total,\
    sales_s,\
    returns_s,\
    _previous_month,\
    _previous_year,\
    _next_month,\
    _next_year,\
    _has_next = get_sales(api = api, id = id, year = year, month = month)

    if validate and not operations: return

    quorum.debug("Sending activity email to %s <%s>" % (name, email))
    quorum.send_mail(
        subject = ACTIVITY_SUBJECT[config.LOCALE] % (target_s, now_s),
        sender = config.SENDER_EMAIL,
        receivers = ["%s <%s>" % (name, email)],
        rich = "email/activity.%s.html.tpl" % config.LOCALE,
        context = dict(
            settings = dict(
                logo = True,
                links = links
            ),
            target = target_s,
            operations = operations,
            sales_total = sales_total,
            sales_count = len(sales_s),
            returns_count = len(returns_s),
            base_url = config.BASE_URL,
            omnix_base_url = config.OMNI_URL,
            commission_rate = config.COMMISSION_RATE
        )
    )

def get_date(year = None, month = None, pivot = config.FIRST_DAY):
    now = datetime.datetime.utcnow()
    year = year or now.year
    month = month or now.month

    has_next = int("%04d%02d" % (year, month)) < int("%04d%02d" % (now.year, now.month))

    previous_month, previous_year = (month - 1, year) if not month == 1 else (12, year - 1)
    next_month, next_year = (month + 1, year) if not month == 12 else (1, year + 1)

    start_month, start_year = (month, year) if now.day >= pivot else (previous_month, previous_year)
    if pivot == config.FIRST_DAY: end_month, end_year = start_month, start_year
    else: end_month, end_year = (start_month + 1, start_year) if not start_month == 12 else (1, start_year + 1)

    start = datetime.datetime(
        year = start_year,
        month = start_month,
        day = pivot
    )
    end = datetime.datetime(
        year = end_year,
        month = end_month,
        day = pivot
    )

    start_t = calendar.timegm(start.utctimetuple())
    end_t = calendar.timegm(end.utctimetuple())

    target = datetime.datetime(year = end_year, month = end_month, day = 1)
    target = target.strftime("%B %Y")

    return (
        target,
        month,
        year,
        start_t,
        end_t,
        previous_month,
        previous_year,
        next_month,
        next_year,
        has_next
    )

def get_top(api = None, year = None, month = None):
    api = api or logic.get_api()

    target, \
    month, \
    year, \
    start_t, \
    _end_t, \
    previous_month, \
    previous_year, \
    next_month, \
    next_year, \
    has_next = get_date(year = year, month = month)

    stats = api.stats_employee(
        date = start_t,
        unit = "month",
        span = 1,
        has_global = True
    )

    top_employees = []
    for object_id, values in stats.items():
        values = values["-1"]
        values["object_id"] = object_id
        values["amount_price_vat"] = values["amount_price_vat"][0]
        values["number_sales"] = values["number_sales"][0]
        top_employees.append(values)

    top_employees.sort(
        reverse = True,
        key = lambda value: value["amount_price_vat"]
    )

    return (
        top_employees,
        target,
        previous_month,
        previous_year,
        next_month,
        next_year,
        has_next
    )

def get_sales(api = None, id = None, year = None, month = None):
    api = api or logic.get_api()

    target, \
    month, \
    year, \
    start_t, \
    end_t, \
    previous_month, \
    previous_year, \
    next_month, \
    next_year, \
    has_next = get_date(year = year, month = month, pivot = config.COMMISSION_DAY)

    kwargs = {
        "filter_string" : "",
        "start_record" : 0,
        "number_records" : -1,
        "sort" : "date:descending",
        "filters[]" : [
            "date:greater:" + str(start_t),
            "date:lesser:" + str(end_t)
        ]
    }
    if id: kwargs["filters[]"].append("primary_seller:equals:" + str(id))
    sales = api.list_sales(**kwargs) if id else api.self_sales(**kwargs)

    kwargs = {
        "filter_string" : "",
        "start_record" : 0,
        "number_records" : -1,
        "sort" : "date:descending",
        "filters[]" : [
            "date:greater:" + str(start_t),
            "date:lesser:" + str(end_t)
        ]
    }

    if id: kwargs["filters[]"].append("primary_return_processor:equals:" + str(id))
    returns = api.list_returns(**kwargs) if id else api.self_returns(**kwargs)

    operations = returns + sales

    sorter = lambda item: item["date"]
    operations.sort(key = sorter, reverse = True)

    sales_total = 0
    for sale in sales: sales_total += sale["price"]["value"]
    for _return in returns: sales_total -= _return["price"]["value"]

    for operation in operations:
        date = operation["date"]
        date_t = datetime.datetime.utcfromtimestamp(date)
        operation["date_f"] = date_t.strftime("%b %d, %Y")

    return (
        operations,
        target,
        sales_total,
        sales,
        returns,
        previous_month,
        previous_year,
        next_month,
        next_year,
        has_next
    )
