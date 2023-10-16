"""send"""
import os
import random

import pika
from dotenv import load_dotenv

load_dotenv()


def multiplayer(text: str) -> str:
    """multiplayer"""
    return text + "." * random.randint(1, 10)  # nosec


class Producer:
    def __init__(self, durable: bool = False) -> None:
        self._connection = None
        self.durable = durable

    def connection(self):
        if not self._connection:
            self.credentials = pika.PlainCredentials(
                os.getenv("RABBITMQ_USERNAME"), os.getenv("RABBITMQ_PASSWORD")
            )
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    os.getenv("RABBITMQ_HOST"), 5672, "/", self.credentials
                )
            )

        return self._connection

    def close(self):
        if self._connection:
            self._connection.close()

    def send(self, message, queue_name: str):
        channel = self.connection().channel()
        channel.queue_declare(queue=queue_name, durable=self.durable)
        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
        print(" [x] Sent '{}'".format(message))
        channel.close()


if __name__ == "__main__":
    producer = Producer(durable=True)
    for counter in range(100):
        producer.send(message=multiplayer("Hello World!"), queue_name="task_queue")
    producer.close()
