from flask import Blueprint, redirect, render_template, request, url_for, flash, session
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Show , show_list, Rating_Review
from . import db
from datetime import date

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
    user_list = show_list(user = new_user, type = "default", name = "Completed")
    fav_list = show_list(user = new_user, type = "default", name = "Favourite")
    db.session.add(new_user)
    db.session.add(user_list)
    db.session.add(fav_list)
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
        # print(currentUser.show_list)
        shows = currentUser.getCompleted_List().shows # return an array of movie object
        shows2 = currentUser.getFavourite_List().shows # return an array of movie object
        # print(currentUser.getCompleted_List())
        return render_template('profile.html', shows = shows, shows2 = shows2, currentUser = currentUser)
    
    return render_template('profile.html', currentUser = currentUser)
    
@auth.route('/add_show', methods=['POST'])
def add_show():
    #get User object to reference fields
    currentUser = User.query.filter_by(id = session['user']).first()

    # show information
    show_type = request.form.get('show_type')
    id = request.form.get('id')
    imgURL = request.form.get('img')
    name = request.form.get('name')
    link = request.form.get('link')

    #check if show exists in db, then add show to the list
    show = Show.query.filter_by(show_id = id).first()
    if not show:
        show = Show(imgURL = imgURL, name = name, show_id = id,
                       info_link = link, show_type = show_type)
        db.session.add(show)
    
    type = request.form.get('type')
    list_name = request.form.get('list_name')
    print(currentUser.show_list)
    currentUser.getShowList(type, list_name).shows.append(show)
    db.session.commit()
    
    return redirect('/profile')

@auth.route('/modify_list/<string:type>/<string:list_name>')
@login_required
def modify_list(type, list_name):
    #get User object to reference fields
    currentUser = User.query.filter_by(id = session['user']).first()

    #if user is logged in, return profile page with movies being an array of Movie objects
    if session['user']:

        # print(type,list_name)
        shows = currentUser.getShowList(type, list_name).shows # return an array of movie object
        return render_template('modify.html', shows = shows, name = list_name, type = type)
    
    return render_template('modify.html')

@auth.route('/delete_show', methods=['POST'])
def remove_show():
    #get User object to reference fields
    currentUser = User.query.filter_by(id = session['user']).first()

    #get show object
    id = request.form.get('id')
    show = Show.query.filter_by(show_id = id).first()
    type = request.form.get('type')
    list_name = request.form.get('list_name')
    if currentUser.getShowList(type, list_name).checkShow(show):
        currentUser.getShowList(type, list_name).shows.remove(show)
        db.session.commit()
    
    # print(type,list_name)
    shows = currentUser.getShowList(type, list_name).shows # return an array of movie object
    return render_template('modify.html', shows = shows, name = list_name, type = type)



@auth.route('/rate_review', methods= ['POST'])
def rate_review():
    #get User object to reference fields
    currentUser = User.query.filter_by(id = session['user']).first()

    # show information
    show_type = request.form.get('show_type')
    id = request.form.get('id')
    imgURL = request.form.get('img')
    name = request.form.get('name')
    link = request.form.get('link')

    #check if show exists in db, then add show to the list
    show = Show.query.filter_by(show_id = id).first()
    if not show:
        show = Show(imgURL = imgURL, name = name, show_id = id,
                       info_link = link, show_type = show_type)
        db.session.add(show)

    # rating_review information
    rating = request.form.get('rating')
    review = request.form.get('review')
    date_time = date.today().strftime("%B %d, %Y")

    # create new review
    userReview = Rating_Review(rating = rating, review = review, user = currentUser, show = show, date_time = date_time)
    db.session.add(userReview)
    db.session.commit()
    print(userReview.user.name)
    print(userReview.show.name)

    return redirect(request.referrer)
    
@auth.route('/recommend')
@login_required
def recommend():
    return render_template('recommend.html')
