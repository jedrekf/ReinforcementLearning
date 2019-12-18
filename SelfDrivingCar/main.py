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
from environment import Env
from agent import SimpleAgent
from displayimg import *

# initialize our server
sio = socketio.Server()
# our flask (web) app
app = Flask(__name__)
# init our model and image array as empty

#AGENT's knowledge about environment
env = Env(MAX_SPEED, MIN_SPEED)
agent = SimpleAgent(env)

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
        pil_image = Image.open(BytesIO(base64.b64decode(data["image"])))
        screen = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
        try:
            new_screen, original_image, m1, m2 = process_img(screen)
            env.update(speed, throttle, steering_angle, [m1, m2])
            steering_angle, throttle = agent.process()
            showimg_nonblock(original_image)
           
            print('sending:: steering angle:{} throttle:{}'.format(steering_angle, throttle))
            send_control(steering_angle, throttle)
        except Exception as e:
            print(e)
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