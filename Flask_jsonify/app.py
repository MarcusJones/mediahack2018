from flask import Flask, render_template, request, Response
from flask import jsonify
import json
import numpy as np
import random
import os
import logging
from time import gmtime, strftime
import datetime
#from astropy._erfa.core import ld
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)8s %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S",
                    )

import operator

import jsonpickle
import numpy as np
#import cv2

from flask_cors import CORS

logging.debug("Started logging")

# Create app
app = Flask(__name__)
# Enable Cross Origin Resource Sharing
CORS(app)

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

    max_sentiment_key = max(sent.items(), key=operator.itemgetter(1))[0]

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
    response = {'message': 'image received. size={}'.format(img.shape)
                }
    
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/soundpush', methods=['POST'])
def soundpush():
    r = request
    
    logging.info('MOCK Soundpush MOCK-> Data received'.format())
    print(r)
    
    #for i in dir(r):
    #    print(i)
    #print(r.content_type)
    #print(r.content_encoding)
    #print(r.content_length)
    #print(r.encoding)
    print("FORM",r.form)
    try:
        print("FILES", r.files)
    except:
        pass
    # convert string of data to uint8
    
    print("DATA",r.data)
    
    file = request.files['data']
    
    
    currtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = file.filename
        print("FILENAME",filename)
        file.save(os.path.join('./SERVER INCOMING', 'audio'+currtime))
        #return redirect(url_for('uploaded_file',
        #                        filename=filename))    
    
    
    
    #nparr = np.fromstring(r.data, np.uint8)
    
    #logging.info('Audio data received. size={}'.format(nparr.shape))
    
    # do some fancy processing here....
    # 
    #
    
    # build a response dict to send back to client
    #response = {'message': 'wav file recieved size={}'.format(nparr.shape)}
    response = {'message': 'wav file recieved'}

    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/soundpush_wav', methods=['POST'])
def soundpush_wav():
    r = request
    logging.info('Soundpush -> Data received'.format())

    # convert string of data to uint8
    nparr = np.fromstring(r.data, np.uint8)

   
    logging.info('Image received. size={}'.format(nparr.shape))
    
    # do some fancy processing here....
    # 
    #
    
    # build a response dict to send back to client
    response = {'message': 'wav file recieved size={}'.format(nparr.shape)
                }
    
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    
    return Response(response=response_pickled, status=200, mimetype="application/json")



if __name__ == "__main__":
        app.run(host='0.0.0.0', debug=True)





from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2

# Initialize the Flask application
app = Flask(__name__)


