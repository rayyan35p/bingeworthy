from flask import Flask, redirect, render_template, url_for, request
import requests
import json

app = Flask(__name__)

# class query_results:
#     def __init__(self, results):
#         self.results = json.loads(results)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    query = request.form['query']
    ##print(query.replace(" ", "+"))
    payload = {'api_key' : '013394cc2a0b549c132a73bfc223372e', 'query' : query}
    r = requests.get('https://api.themoviedb.org/3/search/multi', params=payload)
    print(r.json())
    for value in r.json().get('results'):
        print("id: " + str(value.get('id')))
        try:
            print("title: " + value.get('title'))
        except:
            print("title: " + value.get('name'))

    return render_template('results.html')
    
if __name__ == "__main__":
    app.run(debug=True)