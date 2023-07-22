import pytest
from project import create_app, db, app

# run by running pytest in terminal: pytest
@pytest.fixture
def client():
  app.config["TESTING"] = True
  with app.test_client() as testclient:
    yield testclient

#tests whether homepage is working
def test_home(client):
  response = client.get('/')
  assert b"bingeworthy" in response.data