import numpy as np
import cv2
import time
# import pyautogui
from draw_lanes import draw_lanes
from PIL import Image
from displayimg import *
from config import DRAW_LANES

def roi(img, vertices):
    
    #blank mask:
    mask = np.zeros_like(img)   
    
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, 255)
    
    # showgray(mask)

    #returning the image only where mask pixels are nonzero
    masked = cv2.bitwise_and(img, mask)
    return masked



def process_img(image):
    original_image = image
    # convert to gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # edge detection

    processed_img = cv2.GaussianBlur(processed_img,(5,5),0)

    processed_img =  cv2.Canny(processed_img, threshold1 = 130, threshold2=250)
    
    processed_img = cv2.GaussianBlur(processed_img,(5,5),0)
    
    # showgray(processed_img)
    
    #map this to 320x160
    # vertices = np.array([[10,200],[10,300],[300,200],[500,200],[800,300],[800,500],], np.int32)
    # vertices = np.array( [[[5,70],[315,70],[315,150],[5,150]]], dtype=np.int32 )
    vertices = np.array( [[5,100], [170,50], [315,100], [315,125], [5,125]], dtype=np.int32 )

    processed_img = roi(processed_img, [vertices])

    # showgray(processed_img)

    # more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
    #                                     rho   theta   thresh  min length, max gap:        
    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 20,      10,       15)

    
    l1, l2, m1, b1, m2, b2 = draw_lanes(original_image,lines)
    if DRAW_LANES:
        try:
            cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0,255,0], 5)
            cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0,255,0], 5)
        except Exception as e:
            print(e)
            pass

    return processed_img, original_image, m1, b1, m2, b2


if __name__ == '__main__':
    screen = image = cv2.imread("./images/center_1.jpg")#Image.open("./images/center_1.jpg")

    # cv2.imshow("a", cv2.cvtColor(screen, cv2.COLOR_RGB2HLS))
    # cv2.imshow("b", cv2.cvtColor(screen, cv2.COLOR_RGB2HSV))

    # cv2.waitKey(0) # waits until a key is pressed
    # cv2.destroyAllWindows()

    new_screen,original_image, m1, b1, m2, b2 = process_img(screen)
    #cv2.imshow('window', new_screen)
    cv2.imshow('window_original', original_image)
    cv2.imshow('window_processed',cv2.cvtColor(new_screen, cv2.COLOR_GRAY2BGR))
    
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows()

