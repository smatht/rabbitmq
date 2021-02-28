#!/usr/bin/env python
import os

import pika
import uuid
from dotenv import load_dotenv
load_dotenv()

HOSTNAME = os.environ.get('RABBIT_HOSTNAME')
USERNAME = os.environ.get('RABBIT_USERNAME')
PASSWORD = os.environ.get('RABBIT_PASSWORD')
STR_CON = f'amqp://{USERNAME}:{PASSWORD}@{HOSTNAME}'


class FibonacciRcpClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.URLParameters(STR_CON))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(queue=self.callback_queue,
                                   on_message_callback=self.on_response,
                                   auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id = self.corr_id),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


fibonacci_rpc = FibonacciRcpClient()

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(35)
print(" [.] Got %r" % response)
