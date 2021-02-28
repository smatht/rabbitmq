import json
import time

import pika
import os
from data.destinatarios import DESTINATARIOS
from dotenv import load_dotenv
load_dotenv()

PUB_QUEUE = os.environ.get('RABBIT_QUEUE')

class Connection:
    link = None
    channel = None

    def __init__(self):
        hostname = os.environ.get('RABBIT_HOSTNAME')
        username = os.environ.get('RABBIT_USERNAME')
        password = os.environ.get('RABBIT_PASSWORD')
        parameters = pika.URLParameters(f'amqp://{username}:{password}@{hostname}')
        self.link = pika.BlockingConnection(parameters)
        self.channel = self.link.channel()
        self.channel.queue_declare(queue=PUB_QUEUE, durable=True)


if __name__ == "__main__":
    con = Connection()
    count = 1
    while True:
        if con.channel.is_open:
            for i in range(5):
                message = json.dumps(DESTINATARIOS[i])
                con.channel.basic_publish(
                    exchange='',
                    routing_key=PUB_QUEUE,
                    body=json.dumps(message, ensure_ascii=False),
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # hacer que el mensaje sea persistente
                    ))
        count += 1
        time.sleep(30)
