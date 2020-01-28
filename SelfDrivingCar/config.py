RUNNING_MODE_TRAIN = False
MAX_SPEED = 25
MIN_SPEED = 10
ANGLE_CHANGE = 0.1 # minimum angle change
#how big should be the intervals for a line position
SLOPE_INTERVAL = 0.05 #kind of assumed the 90 angle here
MAX_SLOPE = 4 # max m value of y = mx + b, for detected lines

#how big should be the intervals for a line angle
B_INTERVAL = 10 # images are 320x160 px so it results in 32 width table
IMG_WIDTH = 320
IMG_HEIGHT = 160
MAX_ANGLE = 1

#RL params
ALPHA = 0.9 #learning rate
GAMMA = 0.75 #discount factor
#epsilong greedy params
EPS_MIN = 0.2 # minimum eps
START_EPS = 1 #starting eps
EPS_DECAY = 0.998 # how fast eps decays

TIME_LIMIT = 30 # in seconds
INITIAL_FULL_RANDOM = 0
DRAW_LANES = False
SAVE_Q_SIM_COUNT = 50 # number of episodes after which save current Q table
#if the car for 15 frames doesnt go over 1 mph then restart simulation
LAST_SPPED_FRAMES = 15
STOP_SPEED = 0.99 