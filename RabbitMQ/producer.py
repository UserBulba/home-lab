"""Producer module."""
import os
import random

import debugpy
import pika
from dotenv import load_dotenv

from private.rabbit import RabbitConnection
from private.utility import *

load_dotenv()

# Initialize logger
logger = Logger(__name__, level=os.getenv("MODE", "INFO").upper()).get_logger()
logger.info(f"Log level: {logger.getEffectiveLevel()}")

# Setup debugpy.
debug = os.getenv("MODE", None)
if debug == "DEBUG":
    debugpy.listen(("0.0.0.0", 5678))  # nosec
    debugpy.wait_for_client()
    logger.debug("Waiting for debugger attach")


# Function to generate random dots.
def multiplayer(text: str) -> str:
    """multiplayer"""
    return text + "." * random.randint(1, 10)  # nosec


class Producer:
    def __init__(self, durable: bool = False) -> None:
        self._connection = None
        self.durable = durable

        # Exchange details.
        self.exchange_type = "topic"
        self.exchange = "stocks"

    def connection(self):
        if not self._connection:
            self.credentials = pika.PlainCredentials(
                os.getenv("RABBITMQ_USERNAME"), os.getenv("RABBITMQ_PASSWORD")
            )
            try:
                self._connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        os.getenv("RABBITMQ_HOST"), 5672, "/", self.credentials
                    )
                )
            except pika.exceptions.AMQPConnectionError as error:
                logger.error(f"Error connecting to RabbitMQ: {repr(error)}")
                exit(1)

        return self._connection

    def close(self):
        if self._connection:
            try:
                self._connection.close()
            except pika.exceptions.AMQPConnectionError as error:
                logger.error(f"Error closing RabbitMQ connection: {repr(error)}")

    def send(self, message: str, binding_key: str) -> None:
        channel = self.connection().channel()
        try:
            channel.exchange_declare(
                exchange=self.exchange,
                exchange_type=self.exchange_type,
                durable=self.durable,
            )

        except pika.exceptions.ChannelClosed as error:
            logger.error(f"Error declaring queue: {repr(error)}")

        try:
            channel.basic_publish(
                exchange=self.exchange,
                routing_key=binding_key,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ),
            )
            logger.info(" Published '{}'".format(message))
        except pika.exceptions.ChannelClosed as error:
            logger.error(f"Error publishing message: {repr(error)}")
        finally:
            channel.close()


if __name__ == "__main__":
    producer = Producer(durable=True)
    for counter in range(100):
        producer.send(message=multiplayer("Hello World!"), binding_key="price.stock")
    producer.close()
