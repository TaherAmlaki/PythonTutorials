import os
import pika
from uuid import uuid4

from pymongo.errors import ServerSelectionTimeoutError
from marshmallow.exceptions import ValidationError

from . import logger
from .shoppinglistapp import AprioriResultSchema


class RpcClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.response = None
        self.correlation_id = None
        self._serializer = AprioriResultSchema()
        self.credentials = pika.PlainCredentials(username=os.environ["RABBITMQ_USERNAME"],
                                                 password=os.environ["RABBITMQ_PASSWORD"])

    def on_response(self, channel, method, properties, body):
        logger.debug(f"correlation_id:{self.correlation_id} ? properties.correlation_id:{properties.correlation_id}")
        if self.correlation_id == properties.correlation_id:
            self.response = body.decode("utf-8").replace("Infinity", "100")
            logger.debug(f"response received => {self.response}")
            try:
                obj = self._serializer.loads(self.response)
            except ValidationError as ex:
                logger.error(f"Could not load result from RabbitMQ, error={ex}")
            else:
                try:
                    obj.save()
                except ServerSelectionTimeoutError as serr:
                    logger.error(f"could not save deserialized object, got {serr}")
            finally:
                channel.stop_consuming()
                self.connection.close()
                logger.debug("response message is completely done!")

    def send(self, message):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='host.docker.internal',
                                                                            credentials=self.credentials))
        self.channel = self.connection.channel()
        res = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = res.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None
        self.correlation_id = str(uuid4())
        logger.debug(f"send message is => {message}")
        logger.debug(f"self.callback_queue => {self.callback_queue}")
        logger.debug(f"self.correlation_id => {self.correlation_id}")

        self.channel.basic_publish(
            exchange='',
            routing_key='flaskRabbitQ',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.correlation_id,
                delivery_mode=2
            ),
            body=message
        )
        while self.response is None:
            self.connection.process_data_events()
        return self.response
