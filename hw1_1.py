#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 09:01:58 2017

@author: bryanstamey
some code adapted from PickingROI.py
"""

import cv2
import os

# Step 1- RGB equalization
def myHEQ_RGB(img):
    img = cv2.imread(img)                           # import image
    
    row, col, channels = img.shape
    if channels == 3:                               # check that img is color
        blue, green, red = cv2.split(img)           # split channels
    else:                                           # grayscale image
        blue, green, red = img                      # set all channels to image
    
    # equalize channels
    equRed = cv2.equalizeHist(red)
    equGreen = cv2.equalizeHist(green)
    equBlue = cv2.equalizeHist(blue)
    
    # merge & show equalized channels
    global imgRGB
    imgRGB = cv2.merge((equBlue,equGreen,equRed))

    
# Step 2- YCrCb equalization
def myHEQ_YCRCB(img):
    img = cv2.imread(img)
    
    #convert rgb to YCrCb
    imgYCC = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    Y, Cr, Cb = cv2.split(imgYCC)
    
    # equalize Y channel
    equY = cv2.equalizeHist(Y)
    
    # merge, convert to RGB, and show
    imgYCC = cv2.merge((equY,Cr,Cb))
    global imgRGB_YCC
    imgRGB_YCC = cv2.cvtColor(imgYCC, cv2.COLOR_YCR_CB2BGR)

# Step 3- Picking ROI
# adapted from PickingROI.py
def mouseFunc(event, x, y, flags, param):
    #grab references to the global variables
    global refPt, SelectROI    
    if event == cv2.EVENT_LBUTTONDOWN and SelectROI == 1:
        print 'Pick the left top point'
        refPt = [(x,y)]
        SelectROI = 2
    elif event == cv2.EVENT_LBUTTONUP and SelectROI == 2:
        print 'Pick the right bottom point'
        refPt.append((x,y))
        SelectROI = 3
    cv2.imshow(imgname, imgClone)
    enhanceROI(refPt)

# Step 3- Enhancing ROI
def enhanceROI(refPt):
    cv2.imwrite('ROI.jpg', imgClone[refPt[0][1]:refPt[1][1],refPt[0][0]:refPt[1][0],:])
    myHEQ_YCRCB('ROI.jpg')
    cv2.imwrite('HEQ_YCRCB_ROI.jpg', imgRGB_YCC)
    imgComposite = cv2.imread('HEQ_YCRCB_ROI.jpg')
    imgClone[refPt[0][1]:refPt[1][1],refPt[0][0]:refPt[1][0],:] = imgComposite
    os.remove('ROI.jpg')
    os.remove('HEQ_YCRCB_ROI.jpg')
    cv2.imshow(imgname, imgClone)
    cv2.imwrite('HEQ_ROI.png', imgClone)
    

"""
-------------------------------------------------------------------------------
Load a picture
Perform operations
-------------------------------------------------------------------------------
"""
 
imgname = 'nikonfake.png'       # Enter image to load here
img = cv2.imread(imgname)       # Read image
imgClone = img.copy()           # Create image clone

print "Press j for step 1, k for step 2, p for step 3 selection mode, c for"
print "step 3 clear, or esc to end the program."

# Start key press monitoring
while True:
    cv2.imshow(imgname, imgClone)               # show clone image
    cv2.setMouseCallback(imgname, mouseFunc)    # monitor mouse press
    # monitor key input
    key = cv2.waitKey(0)
    ckey = chr(key & 255)
    if key == 27:                               # break on esc
        break;
    # Step 1
    elif ckey == 'j':                           # step 1 on j press
        print "Performing Step 1"
        myHEQ_RGB(imgname)
        cv2.imshow('HEQ_RGB', imgRGB)           # show enhanced image
        cv2.imwrite('HEQ_RGB.png', imgRGB)      # save enhanced image
    # Step 2
    elif ckey == 'k':                           # step 2 on k press
        print "Performing Step 2"
        myHEQ_YCRCB(imgname)
        cv2.imshow('HEQ_YCRCB', imgRGB_YCC)     # show enhanced image
        cv2.imwrite('HEQ_YCRCB.png', imgRGB_YCC)# save enhanced image
    # Step 3
    elif ckey == 'p':                           # enter step 3 selection mode on p
        print 'Entering Selection Mode'
        SelectROI = 1                           # set to 1 to start top left press
    elif ckey == 'c':                           # clear selection on c
        print 'Clear Selection'
        imgClone = img.copy()
        SelectROI = 0
    elif ckey == 27:                            # wait for esc to break loop
        break
print "Closing all windows"                     # destroy open windows when finished
cv2.destroyAllWindows()
