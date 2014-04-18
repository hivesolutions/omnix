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

import omni
import quorum

import logic
import config

MESSAGE_TIMEOUT = 120
""" The amount of seconds before a message is
considered out dated and is discarded from the
queue even without processing """

LOOP_TIMEOUT = 120
""" The time to be used in between reading new
messages from the omni service, this will only be
used in case there's a problem in the client
connection with the queueing service """

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
        if not config.REMOTE: return

        username = config.USERNAME
        password = config.PASSWORD
        if username == None or password == None:
            raise RuntimeError("Missing authentication information")

        self.api = logic.get_api(mode = omni.DIRECT_MODE)

    def connect(self, queue = "default"):
        if not config.REMOTE: return

        while True:
            try:
                quorum.debug("Starting loop cycle in slave ...")
                self.connection = quorum.get_rabbit(force = True)
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue = queue, durable = True)
                self.channel.basic_qos(prefetch_count = 1)
                self.channel.basic_consume(self.callback, queue = queue)
                self.channel.start_consuming()
            except BaseException, exception:
                quorum.error(
                    "Exception while executing - %s" % unicode(exception),
                    log_trace = True
                )

            time.sleep(LOOP_TIMEOUT)

    def disconnect(self):
        if not config.REMOTE: return

    def callback(self, channel, method, properties, body):
        # prints a debug message about the callback call for the message, this
        # may be used latter for debugging purposes (as requested)
        quorum.debug("Received callback for message")

        # loads the contents of the body that is going to be submitted this
        # is considered the payload of the document to be submitted
        document = json.loads(body)

        # retrieves the various attributes of the document that is going to
        # be submitted, making sure that the issue date is correctly formatted
        type = document["_class"]
        object_id = document["object_id"]
        representation = document["representation"]
        issue_date = document["issue_date"]
        issue_date_d = datetime.datetime.utcfromtimestamp(issue_date)
        issue_date_s = issue_date_d.strftime("%d %b %Y %H:%M:%S")

        # verifies if the document is considered to be outdated (timeout passed)
        # in case it's returns immediately printing a message
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

        # resolves the method for the currently retrieved data type (class)
        # this should raise an exception in case the type is invalid
        method = self._resolve_method(type)

        try:
            # calls the proper method for the submission of the document
            # described by the provided object id, in case there's a problem
            # in the request an exception should be raised and handled properly
            method(object_id)
        except BaseException, exception:
            quorum.error("Exception while submitting document - %s" % unicode(exception))
            retries = properties.priority or 0
            retries -= 1
            properties.priority = retries
            if retries >= 0:
                self.channel.basic_publish(
                    exchange = "",
                    routing_key = "omnix",
                    body = body,
                    properties = properties
                )
                quorum.error("Re-queueing for latter consumption (%d retries pending)" % retries)
            else: quorum.error("No more retries left, the document will be discarded")
        else:
            quorum.info("Document submitted with success")

        # marks the message as acknowledged in the message queue server
        # and then prints a debug message about the action
        channel.basic_ack(delivery_tag = method.delivery_tag)
        quorum.info("Marked message as acknowledged in message queue")

    def run(self):
        self.auth()
        self.connect(queue = "omnix")
        self.disconnect()

    def _resolve_method(self, type):
        if type in config.AT_SALE_TYPES:
            return self.api.submit_invoice_at
        elif type in config.AT_TRANSPORT_TYPES:
            return self.api.submit_transport_at
        else:
            raise RuntimeError("Invalid document type")

def run(count = 1):
    for _index in range(count):
        slave = Slave()
        slave.start()
