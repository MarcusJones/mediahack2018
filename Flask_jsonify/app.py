from flask import Flask, render_template, request, Response
from flask import jsonify
import json
import numpy as np
import random
import logging
#from astropy._erfa.core import ld
logging.basicConfig(level=logging.DEBUG)
import operator

import jsonpickle
import numpy as np
import cv2

logging.debug("Started logging")

app = Flask(__name__)

EMOJI_MAP = {
        'happy'     :   'Happy! :)     http://url_happy',
        'sad'       :   'Sad :*(     http://url_happy',
        'neutral'   :   '-neutral- :| http://url_neutral',
        'angry'     :   'ANGRY!!! >:(     http://url_happy', 
    }





@app.route("/")
def index():
        return render_template("index.html")

@app.route('/sentiment')
def sentiment():
    data = {
        'happy':np.random.uniform(),
        'sad':np.random.uniform(),
        'neutral':np.random.uniform(),
        'angry':np.random.uniform(),
        }

    #data = [0.3, 0.5, 0.9]
    
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    logging.info("Returning sentiment: {} ".format(data))
    return response


@app.route('/emoji')
def emoji():
    sent = sentiment().json
    #print(sent.text)
    #for i in dir(sent):
    #    print(i)
    #print(sent.json)
    #print(sent.response)
    max_sentiment_key = max(sent.items(), key=operator.itemgetter(1))[0]
    #print(maxres)
    #emotions = ['Happy! :)', 'Sad :*(', 'ANGRY!!! >:(']
    #print(random.choice(foo))
    
    data = EMOJI_MAP[max_sentiment_key]
    
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    logging.info("Returning emoji: {}".format(data))
    
    return response




@app.route('/imagepush', methods=['POST'])
def imagepush():
    r = request
       
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    logging.info('Image received. size={}'.format(img.shape))
    
    # do some fancy processing here....
    # 
    #
    
    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                }
    
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    
    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/soundpush', methods=['POST'])
def soundpush():
    data = request.data  # data is empty
    print(data)
    # need posted data here
    
    
if __name__ == "__main__":
        app.run(host='0.0.0.0', debug=True)








from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2

# Initialize the Flask application
app = Flask(__name__)


