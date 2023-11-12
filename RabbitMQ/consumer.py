"""Consumer for RabbitMQ"""
import os
import sys
import time

import pika
from dotenv import load_dotenv

from private.rabbit import RabbitConnection
from private.utility import *

load_dotenv()

# Initialize logger
logger = Logger(__name__, level=os.getenv("MODE", "INFO").upper()).get_logger()
logger.info(f"Log level: {logger.getEffectiveLevel()}")


def check_required_env_vars(required_vars: list) -> None:
    for var in required_vars:
        if os.getenv(var) is None:
            logger.error(f"Error: {var} is not set.")
            sys.exit(1)


def main(queue_name: str) -> None:
    """main loop"""

    def callback(ch, method, properties, body):
        logger.info(f" [x] Received {body.decode()}")
        time.sleep(body.count(b"."))
        logger.info(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consume_messages(channel: pika.channel.Channel):
        channel.basic_qos(prefetch_count=5)
        channel.basic_consume(queue=queue_name, on_message_callback=callback)

        logger.info(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()

    try:
        with RabbitConnection(
            host=os.getenv("RABBITMQ_HOST"),
            user=os.getenv("RABBITMQ_USERNAME"),
            password=os.getenv("RABBITMQ_PASSWORD"),
            queue_name=queue_name,
            durable=True,
        ) as channel:
            consume_messages(channel)

    except pika.exceptions.AMQPConnectionError as error:
        logger.error(f"Error closing RabbitMQ connection: {repr(error)}")
        sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Interrupted")
        sys.exit(0)


if __name__ == "__main__":
    required_env_vars = ["RABBITMQ_HOST", "RABBITMQ_USERNAME", "RABBITMQ_PASSWORD"]
    check_required_env_vars(required_env_vars)

    main(queue_name="task_queue")
