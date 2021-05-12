from flask_marshmallow import Marshmallow
from marshmallow_mongoengine import ModelSchema

from .models import (ShoppingListModel, ItemModel,
                     AprioriResultModel, FrequentItemSetModel, RuleResultModel)

ma = Marshmallow()


class ShoppingListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ShoppingListModel
        include_fk = True


class ShortItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        fields = ("id", "name",)


class ShortShoppingListSchema(ma.SQLAlchemyAutoSchema):
    # items = ma.Nested(ShortItemSchema, many=True)

    class Meta:
        model = ShoppingListModel
        fields = ("id", "user_id", "status", "items")
        include_relationships = True
        include_fk = True


class FrequentItemSetSchema(ModelSchema):
    class Meta:
        model = FrequentItemSetModel


class RuleResultSchema(ModelSchema):
    class Meta:
        model = RuleResultModel


class AprioriResultSchema(ModelSchema):
    class Meta:
        model = AprioriResultModel
