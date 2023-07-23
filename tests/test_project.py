import pytest
import responses
from project import create_app, db, app
from project.models import User, Show, show_list

#tests whether homepage is working
def test_homepage(client):
    response = client.get('/')
    assert b"bingeworthy" in response.data


def test_movie_search(client):
    response = client.post('/results', data = {"query": "spiderman"})
    assert b"/movie/" in response.data


def test_signup(client, app):
    response = client.post('/signup', data = {"email": "4@gmail.com", "name":"4", "password":"3"})
    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == "4@gmail.com"

def test_invalid_login(client):
    client.post("/login", data={"email": "test@test.com", "password": "testpassword"})

    response = client.get("/profile")

    assert response.status_code == 302

def test_valid_login(client, app):
    client.post('/signup', data = {"email": "4@gmail.com", "name":"4", "password":"3"})
    client.post("/login", data={"email": "4@gmail.com", "password":"3"})
    response = client.get("/profile")

    assert response.status_code == 200

def test_addMovieToList(client, app):
    client.post('/signup', data = {"email": "4@gmail.com", "name":"4", "password":"3"})
    client.post("/login", data={"email": "4@gmail.com", "password":"3"})
    client.post("/add_show", data={"show_type":"0", "id" : "557",
                                   "img": "https://image.tmdb.org/t/p/w500/gh4cZbhZxyTbgxQPxD0dOudNPTn.jpg" , "name" : "Spider-Man" , "link" : "/movie/557" , "type": "default"
                                   , "list_name":"Completed"})
    with app.app_context():
        assert show_list.query.count() == 2
        assert show_list.query.first().shows[0].show_id == "557"

def test_follow(client, app):
    with app.app_context():
        u1 = User(name='john', email='john@example.com')
        u2 = User(name='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.followed.all() == []
        assert u1.followers.all() == []
        u1.follow(u2)
        db.session.commit()
        assert u1.is_following(u2)== True
        assert u1.followed.count() == 1
        assert u1.followed.first().name == 'susan'
        assert u2.followers.count() == 1
        assert u2.followers.first().name == 'john'
        u1.unfollow(u2)
        db.session.commit()
        assert u1.is_following(u2)== False
        assert u2.followers.count() == 0
        assert u1.followed.count() == 0

    