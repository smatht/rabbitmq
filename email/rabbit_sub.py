import json
import os
import time

import pika
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
        self.channel.queue_declare(queue=PUB_QUEUE)
        self.channel.basic_consume(PUB_QUEUE, self.on_message)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        self.channel.close()

    def on_message(self, channel, method_frame, header_frame, body):
        print('Enviando mail: ', method_frame.delivery_tag)
        data = json.loads(json.loads(body.decode()))
        print(f'Destinatario: {data["nombre"]}')
        print(f'Email: {data["email"]}')
        print(f'Asunto: {data["asunto"]}')
        print(f'Mensaje: {data["cuerpo"]}')
        print('=======================================================================================================')
        print(' ')
        time.sleep(3)
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)


if __name__ == "__main__":
    con = Connection()