import os
from enum import Enum

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    PROPAGATE_EXCEPTIONS = os.getenv("PROPAGATE_EXCEPTIONS", False)
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    POSTGRES_PORT = os.environ["POSTGRES_PORT"]
    POSTGRES_HOST_NAME = os.environ.get("POSTGRES_HOST_NAME", "db")
    POSTGRES_SERVICE_NAME = "postgresql"
    SQLALCHEMY_DATABASE_URI = f"{POSTGRES_SERVICE_NAME}://" \
                              f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST_NAME}:{POSTGRES_PORT}/{POSTGRES_DB}"

    MONGO_USERNAME = os.getenv('MONGO_INITDB_ROOT_USERNAME')
    MONGO_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
    MONGO_DATABASE = os.getenv('MONGO_INITDB_DATABASE')
    MONGO_PORT = os.getenv('MONGODB_PORT')
    MONGO_HOST = os.getenv('MONGODB_HOST')
    MONGO_SERVICE_NAME = "mongodb"
    MONGODB_SETTINGS = {
        "host": f"{MONGO_SERVICE_NAME}://"
                f"{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DATABASE}?authSource=admin",
        "connect": False
    }


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    PROPAGATE_EXCEPTIONS = os.getenv("PROPAGATE_EXCEPTIONS", True)

    SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI.replace(Config.POSTGRES_SERVICE_NAME, "localhost")
    MONGODB_SETTINGS = {
        "host": Config.MONGODB_SETTINGS["host"].replace(Config.MONGO_SERVICE_NAME, "localhost"),
        "connect": Config.MONGODB_SETTINGS["connect"]
    }


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class ProductionConfig(DevelopmentConfig):
    DEVELOPMENT = False
    DEBUG = False
    PROPAGATE_EXCEPTIONS = False


class Environment(Enum):
    BASE = ("base", Config)
    TEST = ("test", TestConfig)
    DEV = ("dev", DevelopmentConfig)
    PROD = ("prod", ProductionConfig)

    @property
    def name(self):
        return self.value[0]

    @property
    def conf_cls(self):
        return self.value[1]

