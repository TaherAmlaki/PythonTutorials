import logging

from flask import Flask

from ShoppingListApp.configs import get_config
from ShoppingListApp.users.login import login_manager


##############################################
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")

file_handler = logging.FileHandler("FlaskApp.log", mode="w")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
##############################################


def create_app(environment="dev"):
    app = Flask(__name__)

    app.config.from_object(get_config(environment))

    from ShoppingListApp.DB.postgresql import db
    db.init_app(app)

    from ShoppingListApp.DB.mongodb import mongodb
    mongodb.init_app(app)

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



