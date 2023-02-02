from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connection string type that has to pass to the SQLAlchemy
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = 'postgresql://<postgres>:<01521504004>@<localhost>/<fastapiDB>'

# The Engine is responsible for the SQLAlchemy to connect with the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# when we want to tuck the SQL database we have to make session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
