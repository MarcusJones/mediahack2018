from flask import Flask, render_template, request, Response
from flask import jsonify
import json
import numpy as np
import random
import os
import logging
from time import gmtime, strftime
import datetime
from contextlib import suppress
#import glob
import re
from keras.models import load_model
#import cv2
import librosa
from skimage.transform import resize

import pyglet

#from astropy._erfa.core import ld
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(funcName)25s() %(levelname)-9s %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S",
                    )
import operator
import jsonpickle
from flask_cors import CORS

logging.debug("Started logging")
path_wts = os.path.join("./SERVER MODELS", "melspectrogram_with_dropouts.h5")
assert os.path.exists(path_wts)

logging.info("Loading model from {}".format(path_wts))
    
MODEL = load_model(path_wts)

logging.info("Loaded model {}".format(MODEL))
MODEL.summary()

# Create app
app = Flask(__name__)

# Enable Cross Origin Resource Sharing
CORS(app)

# EMOJI_MAP = {
#         'happy'     :   'Happy! :)     http://url_happy',
#         'sad'       :   'Sad :*(     http://url_happy',
#         'neutral'   :   '-neutral- :| http://url_neutral',
#         'angry'     :   'ANGRY!!! >:(     http://url_happy',
#     }

EMOJI_MAP = {
        'happy'     :   'happy'  ,
        'sad'       :   'sad'    ,
        'neutral'   :   'neutral',
        'angry'     :   'angry'  ,
    }

TWEET_MAP = {
        'happy'     :   "I love hacking media! #hacking #media"  ,
        'sad'       :   "Why am I here, this code doesn't compile! #sad #demotivated"    ,
        'neutral'   :   "Hello from Media Hackday, I wish I had more sleep #sleepy #sheep",
        'angry'     :   "I hate hacking, I hate Media. #fu #media"  ,
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
    #img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

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

def load_as_binary(path_file):
    blocksize = 1024*100 # Bytes
    #offset = 0
    cnt = 0
    with open(path_file, "rb") as f:
        bdata = f.read(blocksize)
    logging.info("{} kB loaded".format(len(bdata)/1000))
    return bdata

def load_as_wav(path_file):
    path_file = os.path.abspath(path_file)
    logging.info("Loading {}...".format(path_file))
    #aud = pyglet.media.load(path_file, streaming=False)
    #song.play()
    #pyglet.app.run()
    #print(aud)

    return

def get_audio_file(folder_path):
    audio_files = get_files_by_name_ext(folder_path,'audio','audio')
    
    dated_list = list()
    for f in audio_files:
        fname, _ = os.path.splitext(f)

        fname = fname.replace('audio','')
        this_timestamp = datetime.datetime.strptime(fname, "%Y-%m-%d %H:%M:%S")
        dated_list.append((this_timestamp,f))

    dated_list = sorted(dated_list, key=lambda x: x[0])
    most_recent = dated_list.pop()
    logging.info("Most recent audio file {}".format(most_recent[1]))
    path_most_recent = os.path.join(folder_path,most_recent[1])
    return path_most_recent

def reload_audio(folder_path):
    logging.info("Retrieving audio from {}".format(folder_path))
    
    #--------------------------------------------------------- Get the file name
    path_most_recent = get_audio_file(folder_path)
    
    #------------------------------------------------- Different loading formats
    #data = load_as_binary(path_most_recent)
    data = load_as_wav(path_most_recent) 
    
    #---------------------------------------------------------- Convert to numpy
    if 0:
        byte_type = np.uint8
        np_bdata = np.frombuffer(data,dtype=byte_type)
        logging.debug("Converted raw data to numpy array {}: {}".format(byte_type,np_bdata))
        
    return data

def get_log_melspectrum(data, sample_rate=48000):
    melspectrum = librosa.feature.melspectrogram(data, sample_rate)
    log_melspec = librosa.power_to_db(melspectrum, ref=np.max)
    scaled_spec = 1.0 - np.divide(log_melspec, -80.0)
    logging.debug("Processed log mel spectrum".format())
    return resize(scaled_spec, (128, 128)).reshape(128, 128, 1)


def process_audio(audio_array):
    #processed_data = get_log_melspectrum(audio_array)
    
    # Load the file
    #TODO: This is my todo.
    #logging.info("Loaded {}".format(fpath))

    # Convert to np.arr
    TEMP_ARRAY = np.zeros((3, 3))

    return TEMP_ARRAY

def get_files_by_name_ext(folder_path, search_name, search_ext):

    # Filter
    all_files = os.listdir(folder_path)
    filtered_file_list = [f for f in os.listdir(folder_path) if re.match(r'^audio.*\.audio', f)]
    
    #print(filtered_file_list)
    logging.info("Found {} {} files matching '{}' in {}, out of {} total files".format(len(filtered_file_list),
                                                                           search_ext,
                                                                           search_name,
                                                                           folder_path,
                                                                           len(all_files)))

    return filtered_file_list


#def predict(audio_array):
#    logging.info("Predicting on array {}".format(audio_array.shape))
    
def save_file(file_object):
    currtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path_audio_file_saved = os.path.join('./SERVER INCOMING', 'audio'+currtime+'.audio')
    file_object.save(path_audio_file_saved)
    logging.info("File saved; {}".format(path_audio_file_saved))
        
#     try:
#         file.save(path_audio_file_saved)
#         logging.info("File saved; {}".format(path_audio_file_saved))
#     except:
#         logging.error("MOCK File saved; {} MOCK".format(path_audio_file_saved))

    return

def get_model(path_wts):
    """
    Model architecture
    """
    pass
    #logging.info("Intantiated model".format())
    #logging.info("Applied model weights".format())

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
    with suppress(Exception):
        logging.info('form attrib: {}'.format(r.form))
    with suppress(Exception):
        logging.info('data attrib: {}'.format(r.data))
    with suppress(Exception):        
        logging.info('files attrib: {}'.format(r.files))

    #------------------------------------------------------------------ Get file
    if 'audioBlob' in r.files:
        file = r.files['audioBlob']
    else:
        logging.error("****** NO ['data' attribute in r.files!".format())
        file = 'MOCK'
    
    #-------------------------------------------------- Can ignore the form data
    if 'audioBlob' in r.form:
        form_data = r.form['audioChunks']
    else:
        pass
    
    #----------------------------------------------------------------- Save file
    if 'audioBlob' in r.files:    
        save_file(file)
    else:
        logging.error("MOCK No data to save".format())
        

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
    this_tweet = TWEET_MAP[this_emoji]
    
    #------------------------------------------------------------ Build response
    response = {
        'message': 'audio file recieved',
        'emoji':this_emoji,
        'tweet':this_tweet,
                }
    print(response)
    #----------------------------------------------------------- Return response
    response_pickled = jsonpickle.encode(response)
    
    return Response(response=response_pickled, status=200, mimetype="application/json")



if __name__ == "__main__":
        app.run(host='0.0.0.0', debug=True)

