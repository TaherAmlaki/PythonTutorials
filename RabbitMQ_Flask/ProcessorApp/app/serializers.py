from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from app.models import ShoppingListModel, ItemModel


class OnlyItemNameSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        fields = ("name",)


class ItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_instance = True


class ShoppingListSchema(SQLAlchemyAutoSchema):
    items = Nested("ItemSchema", many=True)

    class Meta:
        model = ShoppingListModel
        include_relationships = True
        load_instance = True


shopping_list_serializer = ShoppingListSchema()
item_serializer = ItemSchema()
item_name_serializer = OnlyItemNameSchema()
