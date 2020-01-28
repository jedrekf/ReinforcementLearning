import math
import random
import numpy as np 
from config import *
from helpers import *

class DriverAgent:
    def __init__(self, env, start_eps, eps_decay, random_exp_n):
        self.env = env
        self.i = 0
        slope_int_count = math.ceil((2*MAX_SLOPE)/SLOPE_INTERVAL) + 1
        angle_int_count = math.ceil(2*MAX_ANGLE/ANGLE_CHANGE) + 1
        self.Q = np.zeros([slope_int_count, slope_int_count, angle_int_count])
        self.random_exp_n = random_exp_n
        self.eps = start_eps
        self.eps_decay = eps_decay
        self.sim_count = 1
        self.last_speeds = np.ones(LAST_SPPED_FRAMES)

    def process(self):
        self.i += 1
        #state = (m1, m2)
        state = self.env.current_state
        self.eps = EPS_DECAY * self.eps
        self.eps = max(self.eps, EPS_MIN)

        if  RUNNING_MODE_TRAIN and (self.i < self.random_exp_n or random.random() < self.eps):
            #if exploring take random action = angle
            action = random.randint(0, len(self.Q[state])-1)
            steering_angle = action*ANGLE_CHANGE - MAX_ANGLE
        else:
            #if exploitinig get Best angle for current state
            #np.unravel_index(np.argmax(self.Q[state], axis=None), self.Q[state].shape)
            action = np.argmax(self.Q[state])
            steering_angle = action*ANGLE_CHANGE - MAX_ANGLE

        # calculate the throttle for steering angle
        # lower the throttle as the speed increases
        # if the speed is above the current speed limit, we are on a downhill.
        # make sure we slow down first and then go back to the original max speed.
        if self.env.speed > self.env.speed_limit:
            self.env.speed_limit = MIN_SPEED  # slow down
        else:
            self.env.speed_limit = MAX_SPEED
        throttle = 1.0 - steering_angle ** 2 - (self.env.speed / self.env.speed_limit) ** 2

        return steering_angle, throttle, action

    def updateQ(self, state, new_state, action, reward):
        #update Q table
        self.Q[state][action] = self.Q[state][action] + ALPHA*(reward + GAMMA*np.max(self.Q[new_state]) - self.Q[state][action])


#okay so
# the table is (state,action) -> reward
# state = position of 2 lines ( so the unique combination of 4 values)
# action = resulting steering wheel angle
# reward = expected reward ( there are no real rewards, only punishment for crossing the line)
