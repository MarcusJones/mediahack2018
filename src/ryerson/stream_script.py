import pyaudio
import time
import librosa, librosa.display
from collections import deque
from keras.models import load_model
import numpy as np
import librosa
from skimage.transform import resize
import tensorflow as tf

model = load_model("../../models/melspectrogram_with_dropouts.h5")

def get_log_melspectrum(data, sample_rate=48000):
    melspectrum = librosa.feature.melspectrogram(data, sample_rate)
    log_melspec = librosa.power_to_db(melspectrum, ref=np.max)
    scaled_spec = 1.0 - np.divide(log_melspec, -80.0)
    return resize(scaled_spec, (128, 128)).reshape(128, 128, 1)

window_size = 2.4
chunk = 9600  # number of data points to read at a time
frame_rate = 48000  # time resolution of the recording device (Hz)

# Initialize a fixed window slice of our frame corresponding to 50 ms
sliding_window = deque(maxlen=int(frame_rate * window_size))
sliding_window.extend([0.0] * sliding_window.maxlen)
fulldata = np.array([])

# q = Queue()
recording = True
idx = 0

graph = tf.get_default_graph()

labels = {0: "happy", 1: "neutral", 2: "neutral", 3:"angry"}

def callback(in_data, frame_count, time_info, status):
    sliding_window.extend(np.frombuffer(in_data, dtype=np.float32))
    data = np.array(sliding_window)
    if np.max(data[chunk // 2:chunk]) > 0.2:
        processed_data = get_log_melspectrum(data)
        with graph.as_default():
            predict_proba = model.predict_proba(processed_data.reshape(1, 128, 128, 1))
            emotion_index = np.argmax(predict_proba)
            print(labels[emotion_index])
    return data, pyaudio.paContinue


p = pyaudio.PyAudio()  # start the PyAudio class
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=frame_rate,
                input=True,
                frames_per_buffer=chunk,
                input_device_index=0,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

print("Pyaudio stops")
# close the stream gracefully
stream.stop_stream()

stream.close()