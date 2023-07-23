from flask import Blueprint, redirect, render_template, request, url_for, flash, session
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Show , show_list, Rating_Review
from . import db
from datetime import date

social = Blueprint('social', __name__)

@social.route('/user_search', methods=['POST'])
def profile_search_results():
    name = request.form['name']
    name = "{0}%".format(name)
    user_list = User.query.filter(User.name.like(name)).all()
    print(user_list)
    return render_template('user_search_results.html', user_list = user_list)

@social.route('/profile/<int:id>')
def profile_search(id):
    profile = User.query.filter_by(id = id).first()
    shows =  profile.getCompleted_List().shows # return an array of movie object
    shows2 = profile.getFavourite_List().shows # return an array of movie object
    return render_template('user_search_profile.html', shows = shows, shows2 = shows2, profile = profile)

@social.route('/view_list/<int:id>/<string:type>/<string:list_name>')
@login_required
def view_list(id, type, list_name):
    #get User object to reference fields
    currentUser = User.query.filter_by(id = id).first()
    #if user is logged in, return profile page with movies being an array of Movie objects
    shows = currentUser.getShowList(type, list_name).shows # return an array of movie object
    return render_template('view_list.html', shows = shows, name = list_name, type = type)


@social.route('/follow/<int:id>')
def follow_user(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        #flash('User {} not found.'.format(user.name))
        return redirect(request.referrer)
    if user == current_user:
        #flash('You cannot follow yourself!')
        return redirect(request.referrer)
    current_user.follow(user)
    db.session.commit()
    #flash('You are following {}!'.format(user.name))
    return redirect(request.referrer)

@social.route('/unfollow/<int:id>')
def unfollow_user(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        #flash('User {} not found.'.format(user.name))
        return redirect(request.referrer)
    if user == current_user:
        #flash('You cannot unfollow yourself!')
        return redirect(request.referrer)
    current_user.unfollow(user)
    db.session.commit()
    #flash('You are unfollowing {}!'.format(user.name))
    return redirect(request.referrer)

@social.route('/viewfollowers')
def view_followers():
    currentUser = User.query.filter_by(id = session['user']).first()
    return render_template('view_followers.html', user = currentUser)