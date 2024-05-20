import os
from contextlib import suppress

import pika
from private.utility import *

# Initialize logger
logger = Logger(__name__, level=os.getenv("MODE", "INFO").upper()).get_logger()


class RabbitUtility:
    @staticmethod
    def get_queue_size(connection: pika.channel.Channel, queue_name: str) -> int | None:
        try:
            method_frame, _, _ = connection.basic_get(queue=queue_name)
            if not isinstance(method_frame, pika.spec.Basic.GetOk):
                return None
        except pika.exceptions.ChannelClosedByBroker:
            logger.warning(f"Cannot find queue: {queue_name}")
            return None
        return method_frame.message_count


class RabbitConnection:
    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        port: int = 5672,
    ):
        self.host = host
        self.user = user
        self.password = password
        self.port = port

        logger.info(f"Initialized RabbitConnection: {self.host}:{self.port}")

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

        return self.channel

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logger.error(f"Exception: {repr(exc_type)}")
            logger.error(f"Exception value: {repr(exc_value)}")
            logger.error(f"Traceback: {traceback}")

        with suppress(Exception):
            self.connection.close()
