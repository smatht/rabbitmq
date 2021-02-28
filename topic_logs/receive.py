#!/usr/bin/env python
import datetime
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

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange='topic_logs', queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(f"[{method.routing_key}] {now}: {body.decode()}")


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()