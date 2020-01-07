class Env:
    def __init__(self, speed_limit, min_speed):
        self.speed_limit = speed_limit
        self.min_speed = min_speed
        self.lanes_history = []

    def update(self, speed, throttle, steering_angle, lane_vecs):
        self.speed = speed
        self.throttle = throttle
        self.steering_angle = steering_angle
        #use bisect to put lane vectors(for now only slope values) from cont to discrete
        self.lane_vectors = lane_vecs
