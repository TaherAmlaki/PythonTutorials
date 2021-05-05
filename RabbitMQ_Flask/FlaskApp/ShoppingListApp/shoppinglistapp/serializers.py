from flask_marshmallow import Marshmallow

from .models import ShoppingListModel, ItemModel


ma = Marshmallow()


class ShoppingListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ShoppingListModel
        include_fk = True


class ShortItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        fields = ("name",)


class ShortShoppingListSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Nested(ShortItemSchema, many=True)

    class Meta:
        model = ShoppingListModel
        fields = ("id", "user_id", "status", "items")
        include_fk = True
