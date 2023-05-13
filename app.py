from flask import Flask, redirect, render_template, url_for, request
import urllib3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
if __name__ == "__main__":
    app.run(debug=True)