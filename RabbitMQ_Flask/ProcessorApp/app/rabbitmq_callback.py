import json

import pika
import time

from . import logger
from .db.postgresql import session
from .models import ShoppingListModel
from .serializers import shopping_list_serializer

from .basketModel import aprioriModel


def on_request_received(channel, method, properties, body):
    body = json.loads(body.decode("utf-8"))
    logger.debug(f"received message: {body}")

    shopping_list_obj = shopping_list_serializer.load(body, session=session)

    if shopping_list_obj.status in ["created", "updated"]:
        shopping_list_obj.save_to_db()
    elif shopping_list_obj.status == "deleted":
        shopping_list_objs = ShoppingListModel.find_all_by_user_id(user_id=shopping_list_obj.user_id)
        if shopping_list_objs:
            for obj in shopping_list_objs:
                obj.delete_from_db()

    apriori = aprioriModel.AprioriModel()
    apriori.fit_model(shopping_list_obj.user_id)
    frequent_item_sets = apriori.frequent_item_sets
    rules = apriori.rules
    response = {
        "user_id": shopping_list_obj.user_id,
        "frequentItemSets": frequent_item_sets,
        "rules": rules
    }
    response = json.dumps(response)
    logger.debug(f"response before sending => {response}")
    time.sleep(1)

    try:
        channel.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id,
                delivery_mode=2,
                content_type="application/json"
            ),
            body=response
        )
    except:
        channel.basic_nack(delivery_tag=method.delivery_tag)
    else:
        channel.basic_ack(delivery_tag=method.delivery_tag)
