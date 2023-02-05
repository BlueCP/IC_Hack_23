from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import  Response, request
from webcam import get_brandname
import webcam
import cv2 

camera = cv2.VideoCapture(0)
old_brand_name = ''

app = Flask(__name__)

def handle_request(product_name):
    # Add more processing here in future.
    return

@app.route('/')
def welcome():
    return redirect(url_for('scanning'))

@app.route('/scanning')
def scanning():
    return render_template('result.html')

@app.route('/processing')
def processing():
    input_json = request.json
    if old_brand_name != get_brandname():
        old_brand_name = get_brandname()
        return get_report(old_brand_name)
    return


@app.route('/video_feed')
def video_feed():
    return Response(webcam.gen_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')