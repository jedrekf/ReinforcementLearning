import math
import subprocess
import numpy as np
import codecs, json 
from config import SLOPE_INTERVAL, B_INTERVAL, ANGLE_CHANGE, MAX_SLOPE, SAVE_Q_SIM_COUNT, LAST_SPPED_FRAMES

def check_max(m1, m2):
    #check if slopes of detected lines are within the accepted range
    #if the values are too big just assume max
    if m1 < -MAX_SLOPE:
        m1 = -MAX_SLOPE
    elif m1 > MAX_SLOPE:
        m1 = MAX_SLOPE

    if m2 < -MAX_SLOPE:
        m2 = -MAX_SLOPE
    elif m2 > MAX_SLOPE:
        m2 = MAX_SLOPE
   
    return (m1, m2)

def mtoidx(angle):
    #angle can be <-1,1> we need to map it to the index 
    # so we take <0, 2> / SLOPE_INTERVAL and see where we land
    idx = math.floor((angle+MAX_SLOPE)/SLOPE_INTERVAL)
    return idx

def idxtom(idx):
    angle = idx*SLOPE_INTERVAL - MAX_SLOPE
    return angle

def restart_simulation(agent):
    #since python win32gui is really bad and didnt work
    #this launches a script written in AutoHotKey - that restarts manually the simulator
    #Udacity simulator doesnt have the api to reset the simulation
    print("restarting simulation now...")
    agent.last_speeds = np.ones(LAST_SPPED_FRAMES)
    if agent.sim_count%SAVE_Q_SIM_COUNT == 0:
        print("Serializing Q table after episodes " + str(agent.sim_count))
        serializeQ(agent)
    subprocess.check_call(['restart_sim.exe'])

def serializeQ(agent):
    b = agent.Q.tolist() # nested lists with same data, indices
    json.dump(b, codecs.open('./q_'+str(agent.i)+".json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format

def deserializeQ(filename, agent):
    #when using this most of the values from config should not be changed between runs
    obj_text = codecs.open(filename, 'r', encoding='utf-8').read()
    b_new = json.loads(obj_text)
    agent.Q = np.array(b_new)