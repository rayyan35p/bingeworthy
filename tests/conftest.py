import pytest
import responses
from project import create_app, db
from project.models import User

# run by running pytest in terminal: pytest
@pytest.fixture
def app():
  app = create_app("sqlite://")

  with app.app_context():
    db.create_all()
  yield app

@pytest.fixture()
def client(app):
  return app.test_client()




# def test_login(client):



