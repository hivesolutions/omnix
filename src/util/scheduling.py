#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Omnix System
# Copyright (C) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import datetime

import omni
import quorum

from util import logic
from util import config
from util import business

def load():
    if not config.SCHEDULE: return
    quorum.debug("Loading scheduling tasks ...")
    load_mail()

def load_mail():
    if not config.REMOTE: return
    quorum.weekly_work(tick_mail, weekday = 4, offset = 14400)
    quorum.monthly_work(tick_previous, monthday = 26, offset = 14400)

def tick_previous():
    now = datetime.datetime.utcnow()
    pre_year, pre_month = (now.year - 1, 12) if now.month == 1 else (now.year, now.month - 1)
    tick_mail(year = pre_year, month = pre_month)

def tick_mail(year = None, month = None):
    api = logic.get_api(mode = omni.Api.DIRECT_MODE)
    business.mail_activity_all(
        api = api,
        year = year,
        month = month,
        validate = True,
        links = False
    )
    quorum.debug("Finished sending activity emails")
