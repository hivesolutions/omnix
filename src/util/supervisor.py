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

import time
import json
import threading

import quorum

import config
import logic

LOOP_TIMEOUT = 120
""" The time to be used in between queueing new
messages from the omni service """

MESSAGE_TIMEOUT = 120
""" The amount of seconds before a message is
considered out dated and is discarded from the
queue even without processing """

MESSAGE_RETRIES = 3
""" The number of retries to be used for the message
before it's considered discarded """

class Supervisor(threading.Thread):

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

        url = config.BASE_URL + "omni/login.json"
        contents_s = logic.post_json(
            url,
            authenticate = False,
            username = username,
            password = password
        )
        self.session_id = contents_s["session_id"]

    def auth_callback(self, params):
        self.auth()
        params["session_id"] = self.session_id

    def connect(self, queue = "default"):
        if not config.REMOTE: return

        self.connection = quorum.get_rabbit(force = True)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue = queue, durable = True)

    def disconnect(self):
        if not config.REMOTE: return

        self.connection.close()

    def execute(self):
        # in case the current instance is not configured according to
        # the remote rules the queuing operation is ignored, and so
        # the control flow returns immediately
        if not config.REMOTE: return

        # creates a values map structure to retrieve the complete
        # set of inbound documents that have not yet been submitted
        # to at for the flush operation
        kwargs = {
            "session_id" : self.session_id,
            "filter_string" : "",
            "start_record" : 0,
            "number_records" : 100,
            "sort" : "issue_date:ascending",
            "filters[]" : [
                "issue_date:greater:1356998400",
                "submitted_at:equals:2",
                "document_type:in:1;3"
            ]
        }
        url = config.BASE_URL + "omni/signed_documents.json"
        contents_s = quorum.get_json(
            url,
            auth_callback = self.auth_callback,
            **kwargs
        )
        valid_documents = [value for value in contents_s\
            if value["_class"] in config.AT_SUBMIT_TYPES]

        # starts the counter value to zero, so that we're able to count
        # the number of messages that have been successfully queued to
        # the remote queueing mechanism (for debugging)
        count = 0

        # iterates over all the valid documents that have been found
        # as not submitted and creates a task for their submission
        # then adds the task to the rabbit queue to be processed
        for document in valid_documents:
            try:
                # tries to run the basic publish operation, this operation
                # may fail for a variety of reasons including errors in the
                # underlying library so a reconnection is attempted in case
                # there's an exception raised under this operation
                self.channel.basic_publish(
                    exchange = "",
                    routing_key = "omnix",
                    body = json.dumps(document),
                    properties = quorum.properties_rabbit(
                        delivery_mode = 2,
                        priority = MESSAGE_RETRIES,
                        expiration = str(MESSAGE_TIMEOUT * 1000),
                        timestamp = time.time()
                    )
                )
                count += 1
            except BaseException, exception:
                # prints a warning message about the exception that has just occurred
                # so that it's possible to act on it
                quorum.warning(
                    "Exception in publish (will re-connect) - %s" % unicode(exception),
                    log_trace = True
                )

                # re-tries to connect with the rabbit channels using the currently
                # pre-defined queue system, this is a fallback of the error
                self.connect(queue = "omnix")

        # prints an information message about the new documents that
        # have been queued for submission by the "slaves"
        quorum.info("Queued %d (out of %d) documents for submission" % (count, len(valid_documents)))

    def loop(self):
        while True:
            try: self.execute()
            except BaseException, exception:
                quorum.error(
                    "Exception while executing - %s" % unicode(exception),
                    log_trace = True
                )
            time.sleep(LOOP_TIMEOUT)

    def run(self):
        self.auth()
        self.connect(queue = "omnix")
        try: self.loop()
        finally: self.disconnect()

def run(count = 1):
    for _index in range(count):
        supervisor = Supervisor()
        supervisor.start()
