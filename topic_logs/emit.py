#!/usr/bin/env python
import os
import pika
import sys
from dotenv import load_dotenv
load_dotenv()

HOSTNAME = os.environ.get('RABBIT_HOSTNAME')
USERNAME = os.environ.get('RABBIT_USERNAME')
PASSWORD = os.environ.get('RABBIT_PASSWORD')
STR_CON = f'amqp://{USERNAME}:{PASSWORD}@{HOSTNAME}'

connection = pika.BlockingConnection(
    pika.URLParameters(STR_CON))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(
    exchange='topic_logs', routing_key=routing_key, body=message)
print(" [x] Sent %r:%r" % (routing_key, message))
connection.close()
