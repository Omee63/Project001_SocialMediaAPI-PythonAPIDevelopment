# this is special file that pytest uses. it allows us to define fixtures here.
# these fixtures will be accessible to any of our test under this Test package (sub package also) aka package specific
# form this file we don't need to import it to other test file to use it, Pytest will auto access in this.

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.main import app
from app.database import get_db, Base
from app.oauth2 import create_access_token
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
# @pytest.fixture(scope="module")  # we are changing the Scope of the Fixture to "module",
# unlike "function" Scope the fixture is destroyed during teardown of the last test in the module.
@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# @pytest.fixture(scope="module")
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client
