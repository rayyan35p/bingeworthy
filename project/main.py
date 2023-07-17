import project.config as config
from flask import Blueprint, Flask, redirect, render_template, url_for, request
import requests
import json
from . import db
from .models import User, Show , show_list, Rating_Review

main = Blueprint('main', __name__)

class query_results:
    
    def __init__(self, id, media_type, poster_url):
        self.id = id
        self.media_type = media_type
        self.poster_url = poster_url
    

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('profile.html')

@main.route('/results', methods=['POST'])
def results():
    query = request.form['query']
    #print(query.replace(" ", "+"))
    payload = {'api_key' : config.api_key, 'query' : query}
    # the request only returns the first page of results... need to figure out a way to get the next pages
    r = requests.get('https://api.themoviedb.org/3/search/multi', params=payload)
    if r.json().get('total_results') == 0:
        return render_template('results.html', no_results=1)
    for value in r.json().get('results'):
        print("id: " + str(value.get('id')))
        # because we are using multi in the api instead of just movies or tv shows,
        # the result can have the name stored in either 'title'(movie) or 'name'(series)
        try:
            print("title: " + value.get('title'))
        except:
            print("title: " + value.get('name'))

    results_list = r.json().get('results')
    query_result_list = []
    # some shows can have no posters so remember to handle
    for result in results_list:
        image_url = ""
        try:
            poster_url = "https://image.tmdb.org/t/p/w500" + result.get('poster_path')
        except:
            # placeholder url
            poster_url = "https://image.tmdb.org/t/p/w500/w3rXpniqssYcppC5UwuQfP1scVB.jpg"
        print(image_url)
        query = query_results(result.get('id'), result.get('media_type'), poster_url)
        query_result_list.append(query)
        
    return render_template('results.html', results=query_result_list)
    
@main.route('/movie/<int:id>')
def movie(id):
    payload = {'api_key' : config.api_key}
    r = requests.get('https://api.themoviedb.org/3/movie/' + str(id) , params=payload)
    movie_details = r.json()
    movie_recommendations = requests.get('https://api.themoviedb.org/3/movie/'  + str(id) + '/recommendations', params=payload)
    #print(movie_recommendations.json())
    movie_recommendations_list = movie_recommendations.json().get('results')
    recommendations_list = []
    for movie_recommendation in movie_recommendations_list:
        try:
            poster_url = "https://image.tmdb.org/t/p/w500" + movie_recommendation.get('poster_path')
        except:
            # placeholder url
            poster_url = "https://image.tmdb.org/t/p/w500/w3rXpniqssYcppC5UwuQfP1scVB.jpg"
        query = query_results(movie_recommendation.get('id'), movie_recommendation.get('media_type'), poster_url)
        recommendations_list.append(query)
        if len(recommendations_list) == 5:
            break
    try:
        # poster url
        poster_url = "https://image.tmdb.org/t/p/w500" + movie_details.get('poster_path')        
    except:
        # placeholder url
        poster_url = "https://image.tmdb.org/t/p/w500/w3rXpniqssYcppC5UwuQfP1scVB.jpg"

    title = movie_details.get('title')
    # release_date contains a string of year-month-day, 2001-01-01 eg
    released_date = movie_details.get('release_date').split("-")[0]
    sypnosis = movie_details.get('overview')
    rating = movie_details.get('vote_average')
    # movie_details.get('genres') returns a list of dictionaries : [ {genre1: action}, {genre2:drama}]
    genre_list = movie_details.get('genres')
    id = movie_details.get('id')
    link = "/movie/" + str(id)
    genres = ""
    for items in genre_list:
        genres = genres + items.get('name') + " "

    # Check for Ratings and Reviews by bingeworthy Users
    show = Show.query.filter_by(show_id = id).first()
    return render_template('showinfo.html', title = title, poster = poster_url, released_date = released_date,
                           sypnosis = sypnosis, rating = rating, genres = genres, id = id, link = link, show_type = 0,
                           show = show, recommendations=recommendations_list)

@main.route('/tv/<int:id>')
def tv(id):
    payload = {'api_key' : config.api_key}
    r = requests.get('https://api.themoviedb.org/3/tv/' + str(id) , params=payload)
    tv_details = r.json()
    tv_recommendations = requests.get('https://api.themoviedb.org/3/tv/'  + str(id) + '/recommendations', params=payload)
    # for some reason stranger things has no recommendation; to check
    tv_recommendations_list = tv_recommendations.json().get('results')
    recommendations_list = []
    for tv_recommendation in tv_recommendations_list:
        try:
            poster_url = "https://image.tmdb.org/t/p/w500" + tv_recommendation.get('poster_path')
        except:
            # placeholder url
            poster_url = "https://image.tmdb.org/t/p/w500/w3rXpniqssYcppC5UwuQfP1scVB.jpg"
        query = query_results(tv_recommendation.get('id'), tv_recommendation.get('media_type'), poster_url)
        recommendations_list.append(query)
        if len(recommendations_list) == 5:
            break
    try:
        # poster url
        poster_url = "https://image.tmdb.org/t/p/w500" + tv_details.get('poster_path')        
    except:
        # placeholder url
        poster_url = "https://image.tmdb.org/t/p/w500/w3rXpniqssYcppC5UwuQfP1scVB.jpg"

    title = tv_details.get('name')
    # first_air_date contains a string of year-month-day, 2001-01-01 eg
    released_date = tv_details.get('first_air_date').split("-")[0]
    sypnosis = tv_details.get('overview')
    rating = tv_details.get('vote_average')
    # tv_details.get('genres') returns a list of dictionaries : [ {genre1: action}, {genre2:drama}]
    genre_list = tv_details.get('genres')
    id = tv_details.get('id')
    link = "/tv/" + str(id)
    genres = ""
    for items in genre_list:
        genres = genres + items.get('name') + " "

    # Check for Ratings and Reviews by bingeworthy Users
    show = Show.query.filter_by(show_id = id).first()

    return render_template('showinfo.html', title = title, poster = poster_url, released_date = released_date,
                           sypnosis = sypnosis, rating = rating, genres = genres, id = id, link = link, show_type = 1,
                           show = show, recommendations=recommendations_list)
