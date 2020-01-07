import math
import random
import numpy as np 
from config import MAX_ANGLE, ANGLE_CHANGE, IMG_HEIGHT, IMG_WIDTH, B_INTERVAL, SLOPE_INTERVAL
from helpers import *

class DriverAgent:
    def __init__(self, env, max_rand_count, rand_explore_coeff):
        self.env = env
        self.qtable = QTable()
        self.i = 0
        self.max_rand_count = max_rand_count
        self.rand_explore_coeff = rand_explore_coeff

    def process(self):
        self.i += 1
        lines = self.env.lane_vectors

        if(self.i < self.max_rand_count):
            angle_idx = self.qtable.biggest_reward_action(lines)
            steering_angle = angle_idx*ANGLE_CHANGE - MAX_ANGLE
        else:
            r = random.random()
            if(r < self.rand_explore_coeff):
                steering_angle = random.randint(0, len(self.qtable.grid[lines])) 
            else:
                angle_idx = self.qtable.biggest_reward_action(lines)
                steering_angle = angle_idx*ANGLE_CHANGE - MAX_ANGLE

        # lower the throttle as the speed increases
        # if the speed is above the current speed limit, we are on a downhill.
        # make sure we slow down first and then go back to the original max speed.
        if self.env.speed > self.env.speed_limit:
            self.env.speed_limit = self.env.min_speed  # slow down
        else:
            self.env.speed_limit = self.env.speed_limit
            throttle = 1.0 - steering_angle ** 2 - (self.env.speed / self.env.speed_limit) ** 2

        return steering_angle, throttle

    def update(self, lines, action, reward):
        self.qtable.update_reward(lines, action, reward)

#this will be a dictionary of <(line1_m, line1_b, line2_m, line2_b), actions[]>
class QTable:
    def __init__(self):
        #initialize all rewards to 0
        #in the table the state is based purely on the slope value of the line for now
        self.grid = {}
        for i in np.arange(-1, 1, SLOPE_INTERVAL):
            for j in np.arange(-1, 1, SLOPE_INTERVAL):
                for a in range(math.ceil((2*MAX_ANGLE)/ANGLE_CHANGE)):
                    cell_address = (i,j)
                    if(a == 0):
                        self.grid[cell_address] = [0]
                    self.grid[cell_address].append(0)

    def biggest_reward_action(self, lines):
        idx = np.argmax(self.grid[lines])
        return idx

    def update_reward(self, lines, action, new_reward):
        self.grid[lines][action] = new_reward

#okay so
# the table is (state,action) -> reward
# state = position of 2 lines ( so the unique combination of 4 values)
# action = resulting steering wheel angle
# reward = expected reward ( there are no real rewards, only punishment for crossing the line)

# how to tell if the agent crossed the line??????????????/