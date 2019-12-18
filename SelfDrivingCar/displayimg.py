import cv2
from PIL import Image
import numpy

# pil_image = Image.open("./images/center_1.jpg")
# screen = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
# # screen = image = cv2.imread("./images/center_1.jpg")
# cv2.imshow("img", screen)

# cv2.waitKey(0) # waits until a key is pressed
# cv2.destroyAllWindows()


def showgray(img):
    cv2.imshow('temp', cv2.cvtColor(img, cv2.COLOR_GRAY2BGR))
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows()

def showimg(img):
    cv2.imshow('temp', img)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows()

def showimg_nonblock(img):
    cv2.imshow('live feed', img)
    cv2.waitKey(10)


