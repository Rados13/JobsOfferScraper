from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import json


def local_update_postgres():
    with open("creditentials.json") as json_file:
        data = json.load(json_file)
        return data["database_url"]


# For local sqlite
# SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

# For Postgres 1.local 2. on server
# SQLALCHEMY_DATABASE_URL = local_update_postgres()
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # only for sqlite , connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
