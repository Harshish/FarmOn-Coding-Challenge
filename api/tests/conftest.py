import pytest
from app.main import app
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient


@pytest.fixture(scope="module")
def monkeymodule():
    with pytest.MonkeyPatch.context() as mp:
        yield mp


@pytest.fixture(scope="function")
def client_test(monkeymodule):
    """
    Create an instance of the client.
    :return: yield HTTP client.
    """
    db = AsyncMongoMockClient()["test_db"]
    monkeymodule.setattr("app.db.db.get_db", db)
    return TestClient(app=app)
