import os

import pika

from app.db.postgresql import Base, engine, session
from app.rabbitmq_callback import on_request_received


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    try:
        credentials = pika.PlainCredentials(username=os.environ["RABBITMQ_USERNAME"],
                                            password=os.environ["RABBITMQ_PASSWORD"])
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='host.docker.internal',
                                                                       credentials=credentials,
                                                                       heartbeat=60))
        channel = connection.channel()
        channel.queue_declare(queue="flaskRabbitQ")
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue="flaskRabbitQ",
                              on_message_callback=on_request_received)
        channel.start_consuming()
    except:
        session.remove()
