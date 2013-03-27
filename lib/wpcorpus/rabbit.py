#
# This file is part of wpcorpus
#
# Copyright (c) 2013 by Pavlo Baron (pb at pbit dot org)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from pika import (BlockingConnection,
                  SelectConnection,
                  BasicProperties)

from pika.callback import CallbackManager

#<- stupid hack
def sanitize(self, key):
    if hasattr(key, 'method') and hasattr(key.method, 'NAME'):
        return key.method.NAME

    if hasattr(key, 'NAME'):
        return key.NAME

    if hasattr(key, '__dict__') and 'NAME' in key.__dict__:
        return key.__dict__['NAME']

    return str(key)

CallbackManager.sanitize = sanitize
#stupid hack ->

class Publisher(object):
    connection = None
    channel = None
    exchange = None

    def __init__(self, props):
        self.props = props

    def start(self, exchange):
        self.exchange = exchange
        self.connection = BlockingConnection()
        self.connection.set_backpressure_multiplier(self.props.backpressure)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=exchange,
                                   durable=True, exclusive=False, auto_delete=False)

    def publish(self, status):
        self.channel.basic_publish(exchange="", routing_key=self.exchange,
                                   body=status,
                                   properties=BasicProperties(content_type="text/plain",
                                                              delivery_mode=1))

    def close(self):
        self.connection.close()

class Consumer():
    connection = None
    channel = None
    queue_name = None
    on_message_callback = None

    def __init__(self, props):
        self.props = props

    def start(self, on_message_callback, exchange):
        self.on_message_callback = on_message_callback
        self.connection = BlockingConnection()
        self.connection.set_backpressure_multiplier(self.props.backpressure)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=exchange,
                                   durable=True, exclusive=False, auto_delete=False)
        
        self.channel.basic_consume(self.on_message, exchange, no_ack=True)

        self.channel.start_consuming()

    def on_message(self, a, b, c, message):
        self.on_message_callback(message)
