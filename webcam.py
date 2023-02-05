from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import pathlib
import os, sys
import asyncio
import numpy as np
from PIL import Image
from threading import Thread
from logohunter_adapter import get_model

from brand_recogniser_model.src.logos import match_logo

#make shots directory to save pics
try:
    os.mkdir('shots')
except OSError as error:
    pass

#Load pretrained face detection model
# net = cv2.dnn.readNetFromCaffe('./saved_model/deploy.prototxt.txt', './saved_model/res10_300x300_ssd_iter_140000.caffemodel')

#instatiate flask app
# app = Flask(__name__, template_folder='./templates')

global processing_frame, counter, brand_name, brand_name_buffer
processing_frame = False
brand_name = "walkers"
counter = 0
brand_name_buffer = []

# def record(out):
#     global rec_frame
#     while(rec):
#         time.sleep(0.05)
#         out.write(rec_frame)

def get_brandname():
    global brand_name
    return brand_name

def gen_frames(camera):  # generate frame by frame from camera
    global processing_frame, counter, brand_name_buffer, brand_name

    yolo_mod = get_model(init=True)
    yolo = yolo_mod['yolo']

    while True:
        print(f"Capturing frame {counter}", file=sys.stdout)
        success, frame = camera.read()

        if not success:
            print("Failed to read frame", file=sys.stderr)
            break
        # opencv images are BGR, translate to RGB
        # frame = frame[:, :, ::-1]
        image = Image.fromarray(frame)
        out_pred, image = yolo.detect_image(image)
        image_array = np.asarray(image)

        # print(f"Processing frame {counter}: {image}", file=sys.stdout)

        yolo = yolo_mod['yolo']
        model = yolo_mod['model']
        my_preprocess = yolo_mod['my_preprocess']
        feat_input = yolo_mod['feat_input']
        sim_cutoff = yolo_mod['sim_cutoff']
        bins = yolo_mod['bins']
        cdf_list = yolo_mod['cdf_list']
        input_labels = yolo_mod['input_labels']
        try:
            labels, bbox_list_list, new_frame = match_logo(image_array, out_pred,
                                              (model, my_preprocess),
                                              "no",
                                              (feat_input, sim_cutoff,
                                               bins, cdf_list,
                                               input_labels),
                                              save_img=False,
                                              save_img_path=None)
            frame = new_frame
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            frame = frame[..., ::-1]
            labels = []

        # sort labels by highest confidence
        labels = sorted(labels, key=lambda x: x[1], reverse=True)
        print(f"PREDICT: {labels}", file=sys.stderr)
        if len(labels) > 0:
            brand_name = labels[0][0]
            brand_name_buffer.append(labels[0][0])
            # brand name is most common brand among last 10 frames
            if (len(brand_name_buffer) > 2):
                brand_name_buffer.pop(0)
                values, counts = np.unique(brand_name_buffer, return_counts=True)
                ind = np.argmax(counts)
                brand_name = values[ind]

        if success:
            if not processing_frame:
                processing_frame = True
                wdir = pathlib.Path().resolve()
                # p = os.path.join(wdir, 'shots', f"newest_shot_{counter}.png")
                counter += 1
                # print(f"Writing to {p}", file=sys.stderr)
                # cv2.imwrite(p, frame)

                # analyse the frame with neural network asynchronously
                # asyncio.run(analyse_image(p))
                processing_frame = False

            # if(rec):
            #     rec_frame=frame
            #     frame= cv2.putText(cv2.flip(frame,1),"Recording...", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),4)
            #     frame=cv2.flip(frame,1)

            try:
                ret, buffer = cv2.imencode('.jpg', frame[..., ::-1])
                # frame = cv2.imread(f"{p[:-4]}_logo.png")
                # ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass

        else:
            pass
    yolo.close_session()

def gen_frames2(camera):
    while True:
        succes, frame = camera.read()
        if not succes:
            break

        try:
            ret, buffer = cv2.imencode('.jpg', frame)
            # frame = cv2.imread(f"{p[:-4]}_logo.png")
            # ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            pass
