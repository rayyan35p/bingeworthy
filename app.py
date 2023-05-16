from flask import Flask, redirect, render_template, url_for, request
import requests
import json

app = Flask(__name__)

class query_results:
    
    def __init__(self, id, media_type, poster_url):
        self.id = id
        self.media_type = media_type
        self.poster_url = poster_url
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    query = request.form['query']
    #print(query.replace(" ", "+"))
    payload = {'api_key' : '013394cc2a0b549c132a73bfc223372e', 'query' : query}
    # the request only returns the first page of results... need to figure out a way to get the next pages
    r = requests.get('https://api.themoviedb.org/3/search/multi', params=payload)
    #print(r.json())
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
    
@app.route('/movie/<int:id>')
def movie(id):
    payload = {'api_key' : '013394cc2a0b549c132a73bfc223372e'}
    r = requests.get('https://api.themoviedb.org/3/movie/' + str(id) , params=payload)
    movie_details = r.json()
    return render_template('movies.html', movie_details=movie_details)

@app.route('/tv/<int:id>')
def tv(id):
    payload = {'api_key' : '013394cc2a0b549c132a73bfc223372e'}
    r = requests.get('https://api.themoviedb.org/3/tv/' + str(id) , params=payload)
    tv_details = r.json()
    return render_template('tv.html', tv_details=tv_details)


if __name__ == "__main__":
    app.run(debug=True)