import os
from contextlib import suppress

import pika
from private.utility import *

# Initialize logger
logger = Logger(__name__, level=os.getenv("MODE", "INFO").upper()).get_logger()
logger.info(f"Log level: {logger.getEffectiveLevel()}")


class RabbitConnection:
    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        queue_name: str,
        port: int = 5672,
        durable: bool = True,
    ):
        self.host = host
        self.user = user
        self.password = password
        self.queue_name = queue_name
        self.port = port
        self.durable = durable

        logger.info(
            f"Initialized RabbitConnection: {self.host}:{self.port}/{self.queue_name}"
        )

    def __enter__(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host, port=self.port, credentials=credentials
        )

        try:
            self.connection = pika.BlockingConnection(parameters)

        except pika.exceptions.AMQPConnectionError as error:
            logger.error(f"Error connecting to RabbitMQ: {repr(error)}")
            exit(1)

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=self.durable)

        return self.channel

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logger.error(f"Exception: {repr(exc_type)}")
            logger.error(f"Exception value: {repr(exc_value)}")
            logger.error(f"Traceback: {traceback}")

        with suppress(Exception):
            self.connection.close()