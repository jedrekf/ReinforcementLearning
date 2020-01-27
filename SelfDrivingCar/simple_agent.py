class SimpleAgent:
    def __init__(self, env):
        self.env = env

    def process(self):
        m1, m2 = self.env.current_state
        if m1 < 0 and m2 < 0:
            steering_angle = 0.2
        elif m1 > 0  and m2 > 0:
            steering_angle = -0.2
        else:
            steering_angle = 0.0

        # lower the throttle as the speed increases
        # if the speed is above the current speed limit, we are on a downhill.
        # make sure we slow down first and then go back to the original max speed.
        if self.env.speed > self.env.speed_limit:
            self.env.speed_limit = self.env.min_speed  # slow down
        else:
            self.env.speed_limit = self.env.speed_limit
            throttle = 1.0 - steering_angle ** 2 - (self.env.speed / self.env.speed_limit) ** 2

        return (steering_angle, throttle)
