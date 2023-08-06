from flask_login import UserMixin
from . import db
import project.config as config
from flask import Blueprint, Flask, redirect, render_template, url_for, request, session
import requests


## Many to Many relationship between shows and lists
show_list_table = db.Table('show_list_table',
                      db.Column('list_id', db.Integer, db.ForeignKey('show_list.id')),
                      db.Column('show_id', db.Integer, db.ForeignKey('show.id')))

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imgURL = db.Column(db.String(100))
    name = db.Column(db.String(100))
    show_type = db.Column(db.Integer)
    show_id = db.Column(db.String(100))
    info_link = db.Column(db.String(100))
    genres = db.Column(db.String(1000))
    genre_ids = db.Column(db.String(100))
    
    ratings_reviews = db.relationship('Rating_Review', backref = 'show')

    # Returns an array of reviews object [review1, review2,...]
    def getRating_Reviews(self):
        return self.ratings_reviews
    
    # Returns the average rating
    def getAverageRating(self):
        total = 0
        count = 0
        for reviews in self.getRating_Reviews():
            total += reviews.rating
            count += 1
        return total/count
    
    def hasRating(self):
        count = 0
        for reviews in self.getRating_Reviews():
            count += 1
        return count != 0


class show_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100)) # custom or default
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shows = db.relationship('Show', secondary = show_list_table, backref = 'show_list')

    #Checks if a show is already in the list, takes in an Object of type Show
    #Returns true/false
    def checkShow(self, show):
        if isinstance(show, Show):
            return show in self.shows
        return False   
    
    def checkShowID(self, id):
        for show in self.shows:
            if show.show_id == str(id): 
                return True
        return False   
    
    #returns eg [[18, 19, ... ], [878, 41, ... ]]
    def get_genre_lists(self):
        movie_genre_list = []
        tv_genre_list = []
        for show in self.shows:
            genre_ids = show.genre_ids.split(",")
            for genre_id in genre_ids:
                if show.show_type == 0:
                    movie_genre_list.append(genre_id)
                else:
                    tv_genre_list.append(genre_id)
        return [movie_genre_list, tv_genre_list]
    
    def count(self):
        number_of_shows = 0
        for show in self.shows:
            number_of_shows = number_of_shows + 1
        return number_of_shows



 
class Rating_Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    review = db.Column(db.String(300))
    # One to many relationships
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_time = db.Column(db.String(300))

    def getInfo(self):
        return [self.rating, self.review, self.user.name, self.date_time]


#followers many to many list for users
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

# One to One relationship between user and movie_list
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    ratings_reviews = db.relationship('Rating_Review', backref = 'user')
    show_list = db.relationship('show_list', backref= 'user')
    watching = db.Column(db.String(100))

    #followers
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    
    # Returns an array of reviews object [review1, review2,...]
    def getRating_Reviews(self):
        return self.ratings_reviews
    
    def getCompleted_List(self):
        for list in self.show_list:
             if list.type == "default" and list.name == "Completed":
                 return list
    
    def getFavourite_List(self):
        for list in self.show_list:
             if list.type == "default" and list.name == "Favourite":
                 return list

    def getShowList(self, type, name):
        for list in self.show_list:
             if list.type == type and list.name == name:
                 return list
             
    def follow(self, user):
        if not self.is_following(user): 
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    
    def get_all_following(self):
        return self.followed.all()
    
    def set_watching(self, name):
        setattr(self, 'watching', name)
        db.session.commit()

    def get_watching(self):
        return self.watching
    
    def changeName(self, name):
        setattr(self, 'name', name)
        db.session.commit()
             
    
