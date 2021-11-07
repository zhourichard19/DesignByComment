
import cv2
from flask.json import jsonify
import numpy as np # linear algebra

import matplotlib.pyplot as plt
from flask import session
from keras.models import Sequential
from keras.applications.vgg19 import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Flatten, Dense, Conv2D, BatchNormalization, MaxPooling2D, Dropout, SeparableConv2D, AveragePooling2D, GlobalAveragePooling2D
from tensorflow.keras.applications import *
from tensorflow.keras.models import Model,load_model
totalDistractionFrames = 0
camera = cv2.VideoCapture(0)
model = load_model('mobilenetv2_distraction2.h5')
def process_frames():
    temp = 0
    totalDistractionFrames = 0
    totalFrames = 0
    success, frame = camera.read()  # read the camera frame
    if not success:
        return 1 
    else:
        totalFrames +=1
        # print(frame.shape)
        frame2 = cv2.resize(frame,(224,224))
        frame2 = np.reshape(frame2,[1,224,224,3])
        prediction = np.argmax(model.predict(frame2))
        print(prediction)
        # #potentially store rolling average of predictions instead
        # if(prediction == 0):
        #     temp+=1
        # elif(temp>5):
        #     totalDistractionFrames += temp
        #     # session["TotalDistractionFrames"] = totalDistractionFrames
        #     temp = 0
        # else:
            # temp = 0
    # return {"distracted":totalDistractionFrames,"focussed":totalFrames}
    return jsonify({"prediction":int(prediction)})

def gen_frames():
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
