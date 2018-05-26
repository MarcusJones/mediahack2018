from keras.models import load_model
import numpy as np
import soundfile as sf
import librosa
from skimage.transform import resize

model = load_model("../../models/melspectrogram_with_dropouts.h5")

def get_log_melspectrum(data, sample_rate=48000):
    melspectrum = librosa.feature.melspectrogram(data, sample_rate)
    log_melspec = librosa.power_to_db(melspectrum, ref=np.max)
    scaled_spec = 1.0 - np.divide(log_melspec, -80.0)
    return resize(scaled_spec, (128, 128)).reshape(128, 128, 1)




if __name__=="__main__":
    ## y = [3: happy, 1: neutral, 4: sad, 5:angry]
    prob = model.predict_proba(get_log_melspectrum(sf.read("../../data/Audio_Speech_Actors_01-24/Actor_17/03-01-03-01-02-01-17.wav")[0]).reshape(1, 128, 128, 1))
    print("Expected 0, predicted ", np.argmax(prob), "predicted probability", prob)
    prob = model.predict_proba(get_log_melspectrum(sf.read("../../data/Audio_Speech_Actors_01-24/Actor_17/03-01-01-01-02-01-17.wav")[0]).reshape(1, 128, 128, 1))
    print("Expected 1, predicted ", np.argmax(prob), "predicted probability", prob)
    prob = model.predict_proba(get_log_melspectrum(sf.read("../../data/Audio_Speech_Actors_01-24/Actor_17/03-01-04-01-02-01-17.wav")[0]).reshape(1, 128, 128, 1))
    print("Expected 2, predicted ", np.argmax(prob), "predicted probability", prob)
    prob = model.predict_proba(get_log_melspectrum(sf.read("../../data/Audio_Speech_Actors_01-24/Actor_17/03-01-05-01-02-01-17.wav")[0]).reshape(1, 128, 128, 1))
    print("Expected 3, predicted ", np.argmax(prob), "predicted probability", prob)