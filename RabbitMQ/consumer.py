"""Analytics consumer."""
import os
import sys
import time

import debugpy
import pika
from dotenv import load_dotenv

from private.rabbit import RabbitConnection, RabbitUtility
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


def check_required_env_vars(required_vars: list) -> None:
    for var in required_vars:
        if os.getenv(var) is None:
            logger.error(f"Error: {var} is not set.")
            sys.exit(1)


class Analytics:
    def __init__(self, durable: bool = False) -> None:
        self.durable = durable

        # Exchange details.
        self.exchange_type = "topic"
        self.exchange = "stocks"
        self.queue_name = "price"

    def on_open(self, connection: pika.channel.Channel, binding_key: str) -> None:
        try:
            logger.info("Connection opened")

            connection.exchange_declare(
                exchange=self.exchange,
                exchange_type=self.exchange_type,
                durable=self.durable,
            )

            connection.queue_declare(queue=self.queue_name, durable=self.durable)

            connection.queue_bind(
                exchange=self.exchange,
                queue=self.queue_name,
                routing_key=binding_key,
            )

            # print(connection.queue_declare_passive(queue=self.queue_name).method.message_count)

        except pika.exceptions.AMQPConnectionError as error:
            logger.error(f"Error initializing RabbitMQ queue: {repr(error)}")
            sys.exit(1)

    def consume_messages(self, connection: pika.channel.Channel):
        def callback(ch, method, properties, body):
            logger.info(f" [x] Received {body.decode()}")
            time.sleep(body.count(b"."))
            logger.info(" [x] Done")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        try:
            connection.basic_qos(prefetch_count=5)
            connection.basic_consume(
                queue=self.queue_name, on_message_callback=callback
            )

            logger.info("Waiting for messages.")
            connection.start_consuming()
        except pika.exceptions.ChannelWrongStateError as error:
            logger.error(f"Error consuming messages: {repr(error)}")
            sys.exit(1)

    def get(self, binding_key: str) -> None:
        """main loop"""

        try:
            with RabbitConnection(
                host=os.getenv("RABBITMQ_HOST"),
                user=os.getenv("RABBITMQ_USERNAME"),
                password=os.getenv("RABBITMQ_PASSWORD"),
            ) as channel:
                channel.exchange_declare(
                    exchange=self.exchange,
                    exchange_type=self.exchange_type,
                    durable=self.durable,
                )

                self.on_open(connection=channel, binding_key=binding_key)

                queue_size = RabbitUtility.get_queue_size(channel, self.queue_name)
                if isinstance(queue_size, int):
                    logger.info("Current queue size: {}".format(queue_size))
                else:
                    logger.warning("Unable to retrieve queue size.")

                self.consume_messages(connection=channel)

        except pika.exceptions.AMQPConnectionError as error:
            logger.error(f"Error closing RabbitMQ connection: {repr(error)}")
            sys.exit(1)

        except KeyboardInterrupt:
            logger.info("Interrupted")
            sys.exit(0)


if __name__ == "__main__":
    required_env_vars = ["RABBITMQ_HOST", "RABBITMQ_USERNAME", "RABBITMQ_PASSWORD"]
    check_required_env_vars(required_env_vars)

    consumer = Analytics(durable=True)
    consumer.get(binding_key="*.stock")
