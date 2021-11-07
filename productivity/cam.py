import cv2
import numpy as np # linear algebra

import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.applications.vgg19 import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Flatten, Dense, Conv2D, BatchNormalization, MaxPooling2D, Dropout, SeparableConv2D, AveragePooling2D, GlobalAveragePooling2D
from tensorflow.keras.applications import *
from tensorflow.keras.models import Model,load_model
camera = cv2.VideoCapture(0)
model = load_model('mobilenetv2_distraction2.h5')
def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        
        else:
            frame = np.reshape(frame,[1,224,224,3])
            prediction = np.argmax(model.predict(frame))
            print(prediction)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
