from flask_login import UserMixin
from . import db
import project.config as config
from flask import Blueprint, Flask, redirect, render_template, url_for, request
import requests


## Many to Many relationship between movie and lists
movie_list = db.Table('movie_list',
                      db.Column('list_id', db.Integer, db.ForeignKey('completed_show_list.id')),
                      db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #list_id = db.Column(db.Integer, db.ForeignKey('completed_show_list.id'))    
    imgURL = db.Column(db.String(100))
    name = db.Column(db.String(100))
    movie_id = db.Column(db.String(100))
    info_link = db.Column(db.String(100))


class completed_show_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shows = db.relationship('Movie', secondary = movie_list, backref = 'completed_show_list')

# One to One relationship between user and movie_list
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    completed_shows = db.relationship('completed_show_list', backref= 'user', lazy = True, uselist=False)

