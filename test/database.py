from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.main import app
from app.database import get_db, Base
import pytest
from alembic import command

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}' \
                          f'@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:01521504004@localhost:5432/fastapi_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# To create a testing database we are creating another 'override_get_db()' which going to give
# a different session object. And this session object is going to point another Database


# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# here it is going to swap dependency for our testing purpose.
# app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# @pytest.fixture
# def client():
#     # run our code before we run our test
#
#     # Because of this, all table will create in the Test Database according to our Schemas
#     Base.metadata.create_all(bind=engine)
#     yield TestClient(app)
#
#     # run our code after our test finishes
#
#     # this is going to drop all our tables after we run our tests.
#     Base.metadata.drop_all(bind=engine)

# with SqlAlchemy
@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
