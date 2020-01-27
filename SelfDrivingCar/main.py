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
import math
# input output
from io import BytesIO
from config import *
from process import *
import numpy as np
from PIL import Image
from environment import Env
from simple_agent import SimpleAgent
from displayimg import *
from driver_agent import DriverAgent
from helpers import mtoidx, restart_simulation, check_max, deserializeQ
import time
import sys



# initialize our server
sio = socketio.Server()
# our flask (web) app
app = Flask(__name__)
# init our model and image array as empty

#AGENT's knowledge about environment
env = Env(MAX_SPEED, MIN_SPEED)
# agent = SimpleAgent(env)

agent = DriverAgent(env, START_EPS, EPS_DECAY, INITIAL_FULL_RANDOM)
if len(sys.argv) > 1:
    filename = str(sys.argv[1])
    deserializeQ(filename, agent)

current_state = (0,0) 

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
            global current_state
            new_screen, original_image, m1, b1, m2, b2,= process_img(screen)
            # if not RUNNING_MODE_TRAIN and m1 == None:
            #     #if we fail to detect a line just improvise and send 0, 0 and hope we detect next
            #     send_control(0,0)
            # else:
            m1, m2 = check_max(m1, m2)
            next_state = (mtoidx(m1), mtoidx(m2))
            env.update(speed, throttle, steering_angle, current_state, next_state)
            next_reward = env.reward()
            steering_angle, throttle, action = agent.process()
            if RUNNING_MODE_TRAIN:
                agent.updateQ(current_state, next_state, action, next_reward)
            if DRAW_LANES:
                showimg_nonblock(original_image)
            print('sending:: steering angle:{} throttle:{}'.format(steering_angle, throttle))
            send_control(steering_angle, throttle)
            current_state = next_state
            agent.last_speeds[int(agent.i%10)] = speed
            #check if 30 seconds passed or if the car is not moving(probably stuck)
            elapsed_time = time.time() - env.start_time
            if RUNNING_MODE_TRAIN and (elapsed_time >= TIME_LIMIT or sum(agent.last_speeds < 0.1) == len(agent.last_speeds)):
                restart_simulation(agent)
        except Exception as e:
            print(e)
            if RUNNING_MODE_TRAIN:
                print("exception during running simulation, it will restart now")
                restart_simulation(agent)
            else:
                print("lines not found so sending 0 0")
                send_control(0,0)

    else:
        sio.emit('manual', data={}, skip_sid=True)

@sio.on('connect')
def connect(sid, environ):
    global current_state
    agent.sim_count += 1
    print("connect ", sid)
    current_state = (mtoidx(0.5753), mtoidx(-0.4687))
    env.update(0, 0, 0, current_state, None) 
    env.start_time = time.time()
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