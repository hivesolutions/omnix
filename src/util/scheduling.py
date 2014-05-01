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

import calendar
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
    now = datetime.datetime.utcnow()
    today = datetime.datetime(year = now.year, month = now.month, day = now.day)
    tomorrow = today + datetime.timedelta(days = 1)
    tomorrow_tuple = tomorrow.utctimetuple()
    target = calendar.timegm(tomorrow_tuple)
    quorum.interval_work(tick_mail, interval = 86400, initial = target)

def tick_mail():
    api = logic.get_api(mode = omni.DIRECT_MODE)
    business.mail_activity_all(api = api, validate = True, links = False)
    quorum.debug("Finished sending activity emails")
