from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# connection string type that has to pass to the SQLAlchemy
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:01521504004@localhost/fastapiDB'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}' \
                          f'@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# The Engine is responsible for the SQLAlchemy to connect with the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# when we want to tuck the SQL database we have to make session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db  # 'yield' is similar to 'return', but returns a generator object.
    finally:
        db.close()

# connecting to the database using Postgres driver
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapiDB', user='postgres', password='01521504004',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Successfully connected to the Database!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)
