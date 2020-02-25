import cv2
import numpy as np

img = cv2.imread('2019-10-04-181131_Right.jpg')
#img2 = cv2.imread('croped/2019-09-01-163701_8mm.jpg')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#mask = cv2.inRange(hsv,(10, 100, 20), (25, 255, 255) )
mask = cv2.inRange(hsv,(4, 133,  29), (24, 196, 216) )
#(array([ -6, 153,  29]), array([ 24, 183, 129]))
#(array([  4, 133,  45]), array([ 34, 163, 145]))
#(array([  3, 164, 117]), array([ 33, 194, 217]))
#(array([  1, 166, 116]), array([ 31, 196, 216]))
#(array([  4,  67, 164]), array([ 44, 107, 284]))


cv2.imshow('image',img);cv2.imshow("orange", mask);
cv2.waitKey();cv2.destroyAllWindows()
