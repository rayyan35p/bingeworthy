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


        

# One to One relationship between user and movie_list
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    ratings_reviews = db.relationship('Rating_Review', backref = 'user')
    show_list = db.relationship('show_list', backref= 'user')
    # Returns an array of reviews object [review1, review2,...]
    def getRating_Reviews(self):
        return self.ratings_reviews
    
    def getCompleted_List(self):
        for list in self.show_list:
             if list.type == "default" and list.name == "completed":
                 return list
    
    def getFavourite_List(self):
        for list in self.show_list:
             if list.type == "default" and list.name == "favourite":
                 return list

    def getShowList(self, type, name):
        for list in self.show_list:
             if list.type == type and list.name == name:
                 return list
