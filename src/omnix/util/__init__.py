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

from . import business
from . import config
from . import ctt
from . import image
from . import logic
from . import scheduling
from . import slave
from . import supervisor

from .business import mail_birthday_all, mail_activity_all, mail_birthday, mail_activity,\
    get_date, get_top, get_sales
from .ctt import encode_ctt
from .config import LOCAL_PREFIX, REMOTE_PREFIX, LOCAL_URL, REMOTE_URL, REDIRECT_URL,\
    CLIENT_ID, CLIENT_SECRET, FIRST_DAY, SCOPE, AT_SALE_TYPES, AT_TRANSPORT_TYPES,\
    AT_SUBMIT_TYPES, REMOTE, BASE_URL, SENDER_EMAIL, USERNAME, PASSWORD, SCHEDULE,\
    COMMISSION_RATE, COMMISSION_DAY, IMAGE_RESIZE, OMNI_URL, PREFIX
from .image import mask_image
from .logic import get_api, ensure_api, on_auth, start_session, reset_session, get_tokens

from .scheduling import load as load_scheduling
from .slave import run as run_slave
from .supervisor import run as run_supervisor
