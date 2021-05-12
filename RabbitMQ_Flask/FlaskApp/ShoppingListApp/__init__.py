from flask import Flask

from .configs import get_config

from .logging import logger

##############################################


def create_app(environment="dev"):
    app = Flask(__name__)

    app.config.from_object(get_config(environment))

    # initializing databases
    from .db.postgresql import postgredb
    postgredb.init_app(app)

    @app.before_first_request
    def create_tables():
        postgredb.create_all()

    from .db.mongodb import mongodb
    mongodb.init_app(app)

    from .users.login import login_manager
    login_manager.init_app(app)

    from .shoppinglistapp.serializers import ma
    ma.init_app(app)

    from .users.views import user_views
    app.register_blueprint(user_views)

    from .shoppinglistapp.views import site_views
    app.register_blueprint(site_views)

    return app



