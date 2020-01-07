#convert slope angle to the index value of the category it falls into
import math
from config import SLOPE_INTERVAL, B_INTERVAL, ANGLE_CHANGE

def slope_to_index(angle):
    idx = math.floor(angle/SLOPE_INTERVAL)
    return idx
    
def b_to_index(b):
    idx = math.floor(b/B_INTERVAL)
    return idx
