#!/usr/bin/env python
import cv2
def removeGreen(image):
    # convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #lower_val = (36, 25, 25)
    lower_val = (18, 0, 15)
    upper_val = (70,255,255)
    mask = cv2.inRange(hsv, lower_val, upper_val)
    res = cv2.bitwise_and(image,image, mask= mask)
    diff_img = image - res
    return

def removeWhiteLight(image):
    # convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_val = (36, 25, 25)
    upper_val = (71,255,255)
    mask = cv2.inRange(hsv, lower_val, upper_val)
    res = cv2.bitwise_and(image,image, mask= mask)
    diff_img = image - res
    return

def onlyOrange(hsv):
    # convert to HSV

    lower_val = (36, 25, 25)
    upper_val = (71,255,255)
    mask = cv2.inRange(hsv,(4, 133,  29), (24, 196, 216) )
    res = cv2.bitwise_not(hsv,hsv, mask= mask)
    diff_img = hsv - res
    return
