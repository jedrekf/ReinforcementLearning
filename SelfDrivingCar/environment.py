import numpy as np
from helpers import idxtom

class Env:
    def __init__(self, speed_limit, min_speed):
        self.speed_limit = speed_limit
        self.min_speed = min_speed
        self.lanes_history = []

    def update(self, speed, throttle, steering_angle, current_state, next_state):
        self.speed = speed
        self.throttle = throttle
        self.steering_angle = steering_angle
        self.current_state = current_state
        self.next_state = next_state

    def reward(self):
        """
        returns reward for current state
        [
            -1 
                0 
                    -1
        ]
        """
        m1 = idxtom(self.current_state[0])
        m2 = idxtom(self.current_state[1])
        if m1 < 0 and m2 < 0 and self.steering_angle < 0:
            return -1
        if m1 > 0  and m2 > 0 and self.steering_angle > 0:
            return -1
        return 0
