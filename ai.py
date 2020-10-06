import librosa
import numpy as np
from scipy.io import wavfile
import warnings
import time

warnings.filterwarnings("ignore")

from keras.models import load_model
model = load_model('model.hdf5')

classes = [
#    'left', 'go', 'yes', 'down', 'up', 'on', 'right', 'no', 'off', 'stop',
    'up', 'down', 'left', 'right'
]

from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils

label_enconder = LabelEncoder()
y = label_enconder.fit_transform(classes)
classes = list(label_enconder.classes_)

#classes = ["", "", "", "", "", "", "", "", "", ""]
#classes = ['down', 'go', 'left', 'no', 'off', 'on', 'right', 'stop', 'up', 'yes']

def s2t_predict(audio, shape_num=8000):
    prob=model.predict(audio.reshape(1,shape_num,1))
    index=np.argmax(prob[0])
    return classes[index]

import sounddevice as sd
import soundfile as sf

samplerate = 16000  
duration = 1 # seconds
filename = 'tmp.wav'


def ai_magic(obj):
    while True:
        while True:
            mydata = sd.rec(samplerate // 100, samplerate=samplerate,
                channels=1, blocking=True)
            if mydata.max() > 0.5:
                    break
        mydata = sd.rec(int(samplerate * duration), samplerate=samplerate,
            channels=1, blocking=True)
        sd.wait()
        sf.write(filename, mydata, samplerate)

        #reading the voice commands
        test, test_rate = librosa.load('tmp.wav', sr = 16000)
        test_sample = librosa.resample(test, test_rate, 8000)
        pred = s2t_predict(test_sample)

        print("Predicted:", pred)

        if pred == "up":
            obj.move = [0, -1]
        elif pred == "down":
            obj.move = [0, 1]
        elif pred == "left":
            obj.move = [-1, 0]
        elif pred == "right":
            obj.move = [1, 0]
