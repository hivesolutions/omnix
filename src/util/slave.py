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

import json
import time
import datetime
import threading

import quorum

import omnix

MESSAGE_TIMEOUT = 240
""" The amount of seconds before a message is
considered out dated and is discarded from the
queue even without processing """

class Slave(threading.Thread):

    session_id = None
    connection = None
    channel = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def stop(self):
        pass

    def auth(self):
        url = omnix.BASE_URL + "omni/login.json"
        contents_s = omnix.post_json(
            url,
            authenticate = False,
            username = quorum.conf("OMNIX_USERNAME"),
            password = quorum.conf("OMNIX_PASSWORD")
        )
        self.session_id = contents_s["session_id"]

    def connect(self, queue = "default"):
        self.connection = quorum.get_rabbit()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue = queue, durable = True)
        self.channel.basic_qos(prefetch_count = 1)
        self.channel.basic_consume(self.callback, queue = queue)
        self.channel.start_consuming()

    def disconnect(self):
        pass

    def callback(self, channel, method, properties, body):
        document = json.loads(body)
        type = document["_class"]
        object_id = document["object_id"]
        representation = document["representation"]
        issue_date = document["issue_date"]
        issue_date_d = datetime.datetime.utcfromtimestamp(issue_date)
        issue_date_s = issue_date_d.strftime("%d %b %Y %H:%M:%S")

        outdated = not properties.timestamp or\
            properties.timestamp < time.time() - MESSAGE_TIMEOUT
        if outdated:
            channel.basic_ack(delivery_tag = method.delivery_tag)
            quorum.info(
                "Canceling/Dropping %s - %s (%s)" % (
                    type,
                    representation,
                    issue_date_s
                )
            )
            return

        # retrieves the current time and uses it to print debug information
        # about the current document submission to at
        quorum.info(
            "Submitting %s - %s (%s)" % (
                type,
                representation,
                issue_date_s
            )
        )

        try:
            # creates the complete url value for the submission
            # operation and run the submission for the current document
            url = omnix.BASE_URL + "omni/signed_documents/submit_at.json"
            quorum.get_json(
                url,
                session_id = self.session_id,
                document_id = object_id
            )
        except BaseException, exception:
            channel.basic_nack(delivery_tag = method.delivery_tag)
            quorum.error("Exception while submitting document - %s" % unicode(exception))
        else:
            channel.basic_ack(delivery_tag = method.delivery_tag)
            quorum.info("Document submitted with success")

    def run(self):
        self.auth()
        self.connect(queue = "omnix")
        self.disconnect()

def run(count = 1):
    for _index in range(count):
        slave = Slave()
        slave.start()
