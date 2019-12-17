# parsing command line arguments
import argparse
# decoding camera images
import base64
# for frametimestamp saving
from datetime import datetime
# high level file operations
import shutil
# real-time server
import socketio
# web server gateway interface
import eventlet.wsgi
# web framework
from flask import Flask
# input output
from io import BytesIO
from config import *
from process import *
import numpy as np
from PIL import Image

# initialize our server
sio = socketio.Server()
# our flask (web) app
app = Flask(__name__)
# init our model and image array as empty

# and a speed limit
speed_limit = MAX_SPEED


@sio.on('telemetry')
def telemetry(sid, data):
    if data:
        # The current steering angle of the car
        steering_angle = float(data["steering_angle"])
        # The current throttle of the car, how hard to push peddle
        throttle = float(data["throttle"])
        # The current speed of the car
        speed = float(data["speed"])
        # The current image from the center camera of the car
        screen = Image.open(BytesIO(base64.b64decode(data["image"])))
        try:
            print('Frame took {} seconds'.format(time.time()-last_time))
            last_time = time.time()
            new_screen,original_image, m1, m2 = process_img(screen)
            #cv2.imshow('window', new_screen)
            cv2.imshow('window2',cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
            
            if m1 < 0 and m2 < 0:
                steering_angle  = 0.5;
            elif m1 > 0  and m2 > 0:
                steering_angle = -0.5
            else:
                # straight()
                print("straight")
            
            cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))

            prediction_last = datetime.now() - start_prediction
            # lower the throttle as the speed increases
            # if the speed is above the current speed limit, we are on a downhill.
            # make sure we slow down first and then go back to the original max speed.
            global speed_limit
            if speed > speed_limit:
                speed_limit = MIN_SPEED  # slow down
            else:
                speed_limit = MAX_SPEED
            throttle = 1.0 - steering_angle ** 2 - (speed / speed_limit) ** 2

            print('predict time: {}; steering angle:{}; throttle:{}'.format(prediction_last.microseconds / 1000000, steering_angle, throttle))
            send_control(steering_angle, throttle)
        except Exception as e:
            print(e)

        # save frame
        # if args.image_folder != '':
        #     timestamp = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
        #     image_filename = os.path.join(args.image_folder, timestamp)
        #     image.save('{}.jpg'.format(image_filename))
    else:
        sio.emit('manual', data={}, skip_sid=True)


@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send_control(0, 0)


def send_control(steering_angle, throttle):
    sio.emit(
        "steer",
        data={
            'steering_angle': steering_angle.__str__(),
            'throttle': throttle.__str__()
        },
        skip_sid=True)


if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)
    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)