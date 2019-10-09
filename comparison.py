#!/usr/bin/env python
# first class
import numpy as np
import cv2
# Import system lib (filename as parameter)
import sys, os
# file/directory path manipulation
from os.path import basename, dirname
from colors_utils import onlyOrange
import json

class Comparison:
    # https://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/
    # Class Attribute
    img_dir = '/home/jody/frelons/2019/compare'
    threshold = 30
    # Initializer / Instance Attributes
    def __init__(self, background, image):
        self.background_path = background
        self.image_path = image

        self.background=cv2.imread(os.path.join(self.img_dir, self.background_path))
        self.image=cv2.imread(os.path.join(self.img_dir, self.image_path))

    def nothing(self,x):
        pass

    def trackBar(self):
        cv2.namedWindow('Options')
        cv2.createTrackbar('threshold','Options',0,255,self.nothing)
        cv2.setTrackbarPos('threshold', 'Options', self.threshold) # default threshold value

    def diffcanvas(self):
        self.threshold = cv2.getTrackbarPos('threshold','Options')
        self.diff = cv2.absdiff(self.image, self.background)
        self.imask =  self.diff>self.threshold
        canvas = np.zeros_like(self.image, np.uint8)
        canvas[self.imask] = self.image[self.imask]
        #cv2.imshow('VIDEO', canvas)
        return canvas

    def orangeOnly(self, canvas):
        hsv = cv2.cvtColor(canvas, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv,(4, 100,  20), (24, 196, 284))
        return mask

    # instance method
    def description(self):
        return "background {} compared with {} threshold {}".format(self.background_path, self.image_path, self.threshold)



mikey = Comparison('2019-10-04-181121_Right.jpg', '2019-10-04-181131_Right.jpg')

print(mikey.description())
mikey.trackBar()
#mikey.diffcanvas

while(1):
    canvas = mikey.diffcanvas()
    cv2.imshow('VIDEO', canvas)
    gray = cv2.GaussianBlur(canvas, (21, 21), 0)
    cv2.imshow('thresh', gray)
    cv2.imshow('ORANGE', mikey.orangeOnly(gray))

    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
