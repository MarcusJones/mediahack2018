from flask import Flask, render_template, request, Response
from flask import jsonify
import json
import numpy as np
import random
import os
import logging
from time import gmtime, strftime
import datetime
#import glob
import re
#from astropy._erfa.core import ld
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(funcName)25s() %(levelname)-9s %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S",
                    )
import operator
import jsonpickle
#import numpy as np
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

def emoji_from_senti(sent_response):
    
    senti_vec = sent_response.json
    #logging.info("Emoji from {}".format(senti_vec))
    max_sentiment_key = max(senti_vec.items(), key=operator.itemgetter(1))[0]

    this_emoji = EMOJI_MAP[max_sentiment_key]
    logging.info("Emoji {} from {}".format(this_emoji,senti_vec))

    return EMOJI_MAP[max_sentiment_key]

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

def reload_audio(folder_path):
    logging.info("Retrieving audio from {}".format(folder_path))
    audio_files = get_files_by_name_ext(folder_path,'audio','audio')

    dated_list = list()
    for f in audio_files:
        fname, _ = os.path.splitext(f)

        #print(fname)
        fname = fname.replace('audio','')
        #print(fname)
        this_timestamp = datetime.datetime.strptime(fname, "%Y-%m-%d %H:%M:%S")
        #print(this_timestamp)
        dated_list.append((this_timestamp,f))

    #print(dated_list)
    dated_list = sorted(dated_list, key=lambda x: x[0])
    #print(dated_list)
    most_recent = dated_list.pop()
    #print(most_recent)
    logging.info("Most recent audio file {}".format(most_recent[1]))

    path_most_recent = os.path.join(folder_path,most_recent[1])

    #result = np.load(path_most_recent)

    blocksize = 1024*100 # Bytes

    #offset = 0
    cnt = 0
    with open(path_most_recent, "rb") as f:
        bdata = f.read(blocksize)
    logging.info("{} kB loaded".format(len(bdata)/1000))

    return bdata

def process_audio(fpath):

    # Load the file
    #TODO: This is my todo.
    logging.info("Loaded {}".format(fpath))

    # Convert to np.arr
    TEMP_ARRAY = np.zeros((3, 3))

    return TEMP_ARRAY

def get_files_by_name_ext(folder_path, search_name, search_ext):
#     all_files = list()
#     for root, dirs, files in os.walk(folder_path):
#         for this_name in files:
#             thisFilePath = os.path.join(root, this_name)
#             all_files.append(thisFilePath)
#
    #files =

    # Filter
    all_files = os.listdir(folder_path)
    filtered_file_list = [f for f in os.listdir(folder_path) if re.match(r'^audio.*\.audio', f)]

    #for f in os.listdir(folder_path):
    #    print(f)

    #print(filtered_file_list)
    logging.info("Found {} {} files matching '{}' in {}, out of {} total files".format(len(filtered_file_list),
                                                                           search_ext,
                                                                           search_name,
                                                                           folder_path,
                                                                           len(all_files)))

    return filtered_file_list




def predict(audio_array):
    logging.info("Predicting on array {}".format(audio_array.shape))

def save_file(file_object):
    currtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #filename = file.filename
    path_audio_file_saved = os.path.join('./SERVER INCOMING', 'audio'+currtime)
    try:
        file.save(path_audio_file_saved)
        logging.info("File saved; {}".format(path_audio_file_saved))
    except:
        logging.error("MOCK File saved; {} MOCK".format(path_audio_file_saved))

    return

def get_model(path_wts):
    """
    Model architecture
    """

    logging.info("Intantiated model".format())
    logging.info("Loaded weights from {}".format(path_wts))
    logging.info("Applied model weights".format())

    return # Return the model for .predict()

def predict(model,proc_audio_data):
    logging.info("Starting MOCK sentiment prediction".format())
    mock_sentiment =  sentiment()
    return mock_sentiment # Sentiment RESPONSE

@app.route('/soundpush', methods=['POST'])
def soundpush():
    r = request

    logging.info('POST to /soundpush {} '.format(r.content_type))

    #print("DATA",r.data)
    logging.info('content_type: {}'.format(r.content_type))

    logging.info('form attrib: {}'.format(r.form))
    logging.info('data attrib: {}'.format(r.data))
    logging.info('files attrib: {}'.format(r.files))

    #------------------------------------------------------------------ Get file
    if 'data' in r.files:
        file = r.files['data']
    else:
        logging.error("****** NO ['data' attribute in r.files!".format())
        file = 'MOCK'


    #----------------------------------------------------------------- Save file
    save_file(file)

    #-------------------------------------------------------------------- Reload
    audio_data = reload_audio("./SERVER INCOMING")

    #---------------------------------------------------------------- Preprocess
    proc_audio_data = process_audio(audio_data)

    #-------------------------------------------------------- Predict sentimenet
    path_wts = os.path.join("./SERVER MODELS", 'mockweightfile.hd5')
    model = get_model(path_wts)
    senti_vector = predict(model,proc_audio_data)

    #-------------------------------------------------------------- Return emoji
    this_emoji = emoji_from_senti(senti_vector)
    # build a response dict to send back to client
    #response = {'message': 'wav file recieved size={}'.format(nparr.shape)}
    response = {'message': 'audio file recieved', 'emoji':this_emoji}

    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")



@app.route('/soundpushMOCK', methods=['POST'])
def soundpushMOCK():
    r = request

    logging.info('POST to /soundpush {} '.format(r.content_type))
    logging.info('content_type: {}'.format(r.content_type))
    logging.info('form attrib: {}'.format(r.form))
    logging.info('data attrib: {}'.format(r.data))
    logging.info('files attrib: {}'.format(r.files))

    if 'data' in r.files:
        file = r.files['data']
    else:
        file = 'MOCK'
        logging.info('MOCK DATA MOCK'.format())

    currtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if file:
        #filename = file.filename
        path_audio_file_saved = os.path.join('./SERVER INCOMING', 'audio'+currtime)
        logging.info("MOCK File saved; {}".format(path_audio_file_saved))
        #file.save(path_audio_file_saved)
        #return redirect(url_for('uploaded_file',
        #                        filename=filename))



    #nparr = np.fromstring(r.data, np.uint8)

    #logging.info('Audio data received. size={}'.format(nparr.shape))

    # do some fancy processing here....
    #
    #

    # build a response dict to send back to client
    #response = {'message': 'wav file recieved size={}'.format(nparr.shape)}
    response = {'message': 'MOCK audio file recieved'}

    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")



if __name__ == "__main__":
        app.run(host='0.0.0.0', debug=True)



# from flask import Flask, request, Response
# import jsonpickle
# import numpy as np
# import cv2
#
# # Initialize the Flask application
# app = Flask(__name__)


