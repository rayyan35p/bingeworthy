from flask import Blueprint, redirect, render_template,  url_for
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return 'Login'

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    return redirect('/login')

@auth.route('/logout')
def logout():
    return 'Logout'