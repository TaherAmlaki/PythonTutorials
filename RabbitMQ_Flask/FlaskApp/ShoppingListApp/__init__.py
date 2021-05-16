from flask import Flask
from dotenv import load_dotenv

from .configs import Environment

from .log import logger

##############################################


def create_app(environment: str = "DEV"):
    environment = Environment[environment]
    if environment == Environment.TEST:
        """ 
        In test we do not run flask app inside Docker container, therefore we load env directly here.
        Also should user docker-compose.yaml file only for test and for dev and prod user both docker-compose .yml and 
        docker-compose.dev.yml 
        """
        load_dotenv("../env/shoppinglistapp.env")

    app = Flask(__name__,
                static_folder="./static",
                template_folder="./templates",
                instance_relative_config=True)

    app.config.from_object(environment.conf_cls)

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



