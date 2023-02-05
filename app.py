from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import Response
from webcam import get_brandname
import webcam
import cv2
from get_report import get_report

camera = cv2.VideoCapture(0)
global old_brand_name
old_brand_name = ''

app = Flask(__name__, static_folder='staticFiles')

@app.route('/')
def welcome():
    return render_template('camera.html')

@app.route('/processing')
def processing():
    # input_json = request.json
    if old_brand_name != get_brandname():
        old_brand_name = get_brandname()
        return get_report(old_brand_name)
    return

@app.route('/video_feed')
def video_feed():
    return Response(webcam.gen_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')
