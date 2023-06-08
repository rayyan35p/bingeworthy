from flask import Blueprint, redirect, render_template, request, url_for, flash, session
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Movie , completed_show_list
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again')
        return redirect(url_for('auth.login'))
    ## get current user info
    session['user'] = user.id
    

    login_user(user, remember=remember)
    # name is not passed into template if user is logged in automatically
    return render_template('index.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect('/signup')
    
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    user_list = completed_show_list(user = new_user)
    db.session.add(new_user)
    db.session.add(user_list)
    db.session.commit()

    return redirect('/login')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@auth.route('/profile')
@login_required
def profile():
    #get User object to reference fields
    currentUser = User.query.filter_by(id = session['user']).first()

    #if user is logged in, return profile page with movies being an array of Movie objects
    if session['user']:
         movies = currentUser.completed_shows.shows # return an array of movie object
         print(movies)
         return render_template('profile.html', movies = movies)
    
    return render_template('profile.html')
    
@auth.route('/add_movie', methods=['POST'])
def add_movie():
    #get User object to reference fields
    currentUser = User.query.filter_by(id = session['user']).first()

    # movie information
    id = request.form.get('id')
    imgURL = request.form.get('img')
    name = request.form.get('name')
    link = request.form.get('link')
    print(id)

    #check if movie exists in db, then add movie to the list
    movie = Movie.query.filter_by(movie_id = id).first()
    if not movie:
        movie = Movie(imgURL = imgURL, name = name, movie_id = id,
                       info_link = link)
        db.session.add(movie)
        
    currentUser.completed_shows.shows.append(movie)
    db.session.commit()

    return redirect('/profile')