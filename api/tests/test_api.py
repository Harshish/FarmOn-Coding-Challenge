import dotenv
from fastapi.testclient import TestClient

try:
    dotenv.load_dotenv()
except IOError:
    pass


def test_root(client_test: TestClient):
    response = client_test.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"All Creatures Welcome!"}