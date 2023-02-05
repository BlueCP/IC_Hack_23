from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import  Response, request

from logohunter_adapter import get_model#, predict_logo

import cv2
import datetime, time
import os, sys
import numpy as np
import pathlib

from threading import Thread


app = Flask(__name__)

global capture,rec_frame, grey, switch, neg, face, rec, out, camera
capture=0
grey=0
neg=0
face=0
switch=1
rec=0

import webcam

# wdir = pathlib.Path().resolve()
# test_input = os.path.join(wdir, 'test_image.jpg')
# get_model(test_input)


#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

#Load pretrained face detection model    
# net = cv2.dnn.readNetFromCaffe('./saved_model/deploy.prototxt.txt', './saved_model/res10_300x300_ssd_iter_140000.caffemodel')

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')

camera = cv2.VideoCapture(0)

def handle_request(product_name):
    return f'Your product is: {product_name}'

@app.route('/')
def welcome():
    # return redirect(url_for('query'))
    return render_template('camera-example.html')

@app.route('/query')
def query():
    product_name = request.args.get('product_name', '')
    if product_name != '':
        return render_template('result.html', product_name=product_name)
    else:
        return render_template('query.html')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
        elif  request.form.get('grey') == 'Grey':
            global grey
            grey=not grey
        elif  request.form.get('neg') == 'Negative':
            print("Doing test")
            wdir = pathlib.Path().resolve()
            test_input = os.path.join(wdir, 'test_image.jpg')
            get_model(test_input, False)
        elif  request.form.get('face') == 'Face Only':
            global face
            face=not face 
            if(face):
                time.sleep(4)   
        elif  request.form.get('stop') == 'Stop/Start':

            if(switch==1):
                switch=0
                camera.release()
                cv2.destroyAllWindows()

            else:
                camera = cv2.VideoCapture(0)
                switch=1
        elif  request.form.get('rec') == 'Start/Stop Recording':
            global rec, out
            rec= not rec
            if(rec):
                now=datetime.datetime.now() 
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter('vid_{}.avi'.format(str(now).replace(":",'')), fourcc, 20.0, (640, 480))
                #Start new thread for recording the video
                thread = Thread(target = record, args=[out,])
                thread.start()
            elif(rec==False):
                out.release()


    elif request.method=='GET':
        return render_template('camera-example.html')
    return render_template('camera-example.html')

@app.route('/video_feed')
def video_feed():
    return Response(webcam.gen_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')


'''
@app.route('/hello_world')
def hello_world():
    return redirect(url_for('hello'))

@app.route('/any_string/<bar>')
def foo(bar):
    return f'Input string: {bar}'
'''
