from ShoppingListApp.shoppinglistapp.serializers import ma
from .models import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        include_fk = True
        include_relationships = True
        load_only = ("password", )
        dump_only = ("id", )
