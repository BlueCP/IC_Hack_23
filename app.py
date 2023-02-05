from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import Response, jsonify
from webcam import get_brandname
import sys
import webcam
import cv2
from get_report import get_report

camera = cv2.VideoCapture(0)
old_brand_name = ''

app = Flask(__name__, static_folder='staticFiles')

@app.route('/')
def welcome():
    return render_template('camera.html')

@app.route('/processing', methods=['GET'])
def processing():
    input_json = request.json
    print("Received GET request:", file=sys.stdout)
    print(input_json, file=sys.stdout)
    if old_brand_name != get_brandname():
        old_brand_name = get_brandname()
        return jsonify(get_report(old_brand_name))
    return jsonify({})

@app.route('/video_feed')
def video_feed():
    return Response(webcam.gen_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')
