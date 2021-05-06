import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    POSTGRES_PORT = os.environ["POSTGRES_PORT"]
    POSTGRES_HOST_NAME = os.environ.get("POSTGRES_HOST_NAME", "db")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST_NAME}:{POSTGRES_PORT}/{POSTGRES_DB}"

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    PROPAGATE_EXCEPTIONS = os.getenv("PROPAGATE_EXCEPTIONS", True)
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestConfig(DevelopmentConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///shoppinglist.db"


class ProductionConfig(Config):
    PROPAGATE_EXCEPTIONS = os.getenv("PROPAGATE_EXCEPTIONS", False)


def get_config(environment):
    return {
        "dev": DevelopmentConfig,
        "test": TestConfig,
        "prod": ProductionConfig
    }.get(environment, Config)
