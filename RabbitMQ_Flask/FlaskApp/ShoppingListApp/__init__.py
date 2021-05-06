from flask import Flask

from ShoppingListApp.configs import get_config
from ShoppingListApp.users.login import login_manager


def create_app(environment="dev"):
    app = Flask(__name__)

    app.config.from_object(get_config(environment))

    from ShoppingListApp.DB.postgresql import db
    db.init_app(app)

    from ShoppingListApp.DB import mongodb
    mongodb.init()

    @app.before_first_request
    def create_tables():
        db.create_all()
    login_manager.init_app(app)

    from ShoppingListApp.shoppinglistapp.serializers import ma
    ma.init_app(app)

    from ShoppingListApp.users.views import user_views
    app.register_blueprint(user_views)

    from ShoppingListApp.shoppinglistapp.views import site_views
    app.register_blueprint(site_views)

    return app
