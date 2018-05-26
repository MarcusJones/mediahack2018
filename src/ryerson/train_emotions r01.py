import keras
import soundfile as sf
from tqdm import tqdm
from glob2 import glob
import numpy as np
import os
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential, load_model
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import models, layers, optimizers, applications
import matplotlib.pyplot as plt
#import joblib
import librosa
import pandas as pd
from skimage.transform import resize
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping, ModelCheckpoint

from keras.applications.vgg16 import VGG16

from keras.models import Model


#%% 
from keras import backend as K

#intra_op_‌​parallelism_threads=7

#this_config=K.tf.ConfigProto(intra_op_‌​parallelism_threads=7,inter_op_parallelism_threads=7)
this_config = K.tf.ConfigProto(intra_op_parallelism_threads=7)
this_config_sess = K.tf.Session(config = this_config)
K.set_session(this_config_sess)
#%%
def cnn_model(height, width, color_dim):

    model = Sequential()
    model.add(Convolution2D(32, (3, 3), input_shape=(128, 128, 1)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))

    model.add(Convolution2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))

    model.add(Convolution2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))

    model.add(Convolution2D(128, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy']
                 )
    return model


def cnn_vgg16_secondtry():
    img_rows = 128
    img_cols = 128
    img_channels = 3
    base_model = applications.VGG16(weights='imagenet', 
                                    include_top=False, 
                                    input_shape=(img_rows, img_cols, img_channels)
                                    )

def cnn_vgg16():
    #raise
    # Generate a model with all layers (with top)
    vgg16 = VGG16(weights=None, include_top=True)
    
    #Add a layer where input is the output of the  second last layer 
    x = Dense(8, activation='softmax', name='predictions')(vgg16.layers[-2].output)
    
    #Then create the corresponding model 
    my_model = Model(input=vgg16.input, output=x)
    
    summary = my_model.summary()
    print(summary)
            
    return my_model 
#%%
def get_log_melspectrum(data, sample_rate=48000):
    melspectrum = librosa.feature.melspectrogram(data, sample_rate)
    log_melspec = librosa.power_to_db(melspectrum, ref=np.max)
    scaled_spec = 1.0 - np.divide(log_melspec, -80.0)
    return resize(scaled_spec, (128, 128)).reshape(128, 128, 1)

## y = [happy, neutral, sad, angry]
def prepare_data():
    X, y = [], []
    data_path = r"/home/batman/Dropbox/DATA/audio Ryerson/Audio_Speech_Actors_01-24"
    for filepath in glob(data_path + r"/*/*.wav"):
        filename = filepath.split("/")[-1]
        emotion = filename.split("-")[2]
        try:
            if emotion=="03":
                X.append(get_log_melspectrum(sf.read(filepath)[0]))
                y.append([1., 0., 0., 0.])
            elif emotion=="01":
                X.append(get_log_melspectrum(sf.read(filepath)[0]))
                y.append([0., 1., 0., 0.])
            elif emotion=="04":
                X.append(get_log_melspectrum(sf.read(filepath)[0]))
                y.append([0., 0., 1., 0.])
            elif emotion=="05":
                X.append(get_log_melspectrum(sf.read(filepath)[0]))
                y.append([0., 0., 0., 1.])
            else:
                pass
        except:
            pass
    return X, y

def train_model_vgg16(batch_size=32, epochs=100, plot=True):

    #model = cnn_vgg16(128, 128, 1)
    #model = cnn_vgg16()
    model = cnn_vgg16_secondtry()
    filepath = '/home/batman/git/mediahack2018/models/melspectrogram_with_dropouts.h5'
    #print(os.getcwd())
    checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    callbacks_list = [checkpoint]
    history = model.fit(np.array(X_train), np.array(y_train),
                        validation_data=(np.array(X_test), np.array(y_test)),
                        batch_size=batch_size, nb_epoch=epochs, shuffle=True, callbacks=callbacks_list)
    print("Model melspectrogram_with_dropouts.h5 successfully saved")
    if plot:
        plot_training(history)


def train_model(batch_size=32, epochs=100, plot=True):

    model = cnn_model(128, 128, 1)
    
    filepath = '/home/batman/git/mediahack2018/models/melspectrogram_with_dropouts.h5'
    #print(os.getcwd())
    checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    callbacks_list = [checkpoint]
    history = model.fit(np.array(X_train), np.array(y_train),
                        validation_data=(np.array(X_test), np.array(y_test)),
                        batch_size=batch_size, nb_epoch=epochs, shuffle=True, callbacks=callbacks_list)
    print("Model melspectrogram_with_dropouts.h5 successfully saved")
    if plot:
        plot_training(history)

def plot_training(history):
    history_dict = history.history
    loss_values = history_dict['loss']
    validation_loss_values = history_dict['val_loss']
    accuracy_values = history_dict['acc']
    validation_accuracy_values = history_dict['val_acc']
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_figwidth(10)
    ax1.plot(loss_values, 'b', label='Training loss')
    ax1.plot(validation_loss_values, 'r', label='Validation loss')
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('Loss')
    ax1.set_title('Training and Validation loss')
    ax2.plot(accuracy_values, 'b', label='Training accuracy')
    ax2.plot(validation_accuracy_values, 'r', label='Validation accuracy')
    ax2.set_xlabel('Epochs')
    ax2.set_ylabel('Accuracy')
    ax2.set_title('Training and Validation accuracy')
    plt.show()

#%%
if __name__=="__main__":
    X, y = prepare_data()

    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.33,
                                                        random_state=123)
    
    #train_model(batch_size=64, epochs=100)
    
    train_model_vgg16(batch_size=64, epochs=100)
