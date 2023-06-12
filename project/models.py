from flask_login import UserMixin
from . import db
import project.config as config
from flask import Blueprint, Flask, redirect, render_template, url_for, request, session
import requests


## Many to Many relationship between shows and lists
show_list = db.Table('show_list',
                      db.Column('list_id', db.Integer, db.ForeignKey('completed_show_list.id')),
                      db.Column('show_id', db.Integer, db.ForeignKey('show.id')))

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #list_id = db.Column(db.Integer, db.ForeignKey('completed_show_list.id'))    
    imgURL = db.Column(db.String(100))
    name = db.Column(db.String(100))
    show_type = db.Column(db.Integer)
    show_id = db.Column(db.String(100))
    info_link = db.Column(db.String(100))


class completed_show_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shows = db.relationship('Show', secondary = show_list, backref = 'completed_show_list')

    #Checks if a show is already in the list, takes in an Object of type Show
    #Returns true/false
    def checkShow(self, show):
        if isinstance(show, Show):
            return show in self.shows
        return False
        

# One to One relationship between user and movie_list
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    completed_shows = db.relationship('completed_show_list', backref= 'user', lazy = True, uselist=False)

