from flask import Flask, render_template
from flask import jsonify
import json
import numpy as np
import random


app = Flask(__name__)

@app.route("/")
def index():
        return render_template("index.html")

@app.route('/sentiment')
def sentiment():
    data = [
        np.random.uniform(),
        np.random.uniform(),
        np.random.uniform(),
        ]

    #data = [0.3, 0.5, 0.9]
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/emoji')
def emoji():
    

    emotions = ['Happy! :)', 'Sad :*(', 'ANGRY!!! >:(']
    #print(random.choice(foo))
    
    data = random.choice(emotions)
    
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == "__main__":
        app.run(host='0.0.0.0', debug=True)

