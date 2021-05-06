import os
# from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


# load_dotenv()
# POSTGRES_USER = os.environ["POSTGRES_USER"]
# POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
# POSTGRES_DB = os.environ["POSTGRES_DB"]
# POSTGRES_PORT = os.environ["POSTGRES_PORT"]
# SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:{POSTGRES_PORT}/{POSTGRES_DB}"

# engine = create_engine(url=SQLALCHEMY_DATABASE_URI)
engine = create_engine(url="sqlite:///:memory:")
session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
