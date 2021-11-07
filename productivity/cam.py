
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
model = load_model('mobilenetv2_faceonly.h5')
face_model = cv2.CascadeClassifier('lbpcascade_frontalface_improved.xml')
def process_frames():
    temp = 0
    totalDistractionFrames = 0
    totalFrames = 0
    success, frame = camera.read()  # read the camera frame
    if not success:
        return 1 
    else:
        predictions = []
        totalFrames +=1
        faces=face_model.detectMultiScale(frame)
        for (x,y,w,h) in faces:
            face_img=frame[y:y+w,x:x+w]
            # print(frame.shape)
            frame2 = cv2.resize(face_img,(224,224))
            frame2 = np.reshape(frame2,[1,224,224,3])
            prediction = np.argmax(model.predict(frame2))
            predictions.append(prediction)
        #potentially store rolling average of predictions instead
        output = 1 if not len(faces) else max(predictions)
    return jsonify({"prediction":int(output)})

def gen_frames():
    
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            faces=face_model.detectMultiScale(frame)
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),"green",2)
                # cv2.rectangle(frame,(x,y-40),(x+w,y),"green",-1)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
