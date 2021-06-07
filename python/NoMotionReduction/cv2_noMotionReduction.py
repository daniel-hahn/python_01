'''
Created on 27 Oct 2020
@author: dan

this program extracts the movement of bacterial growth shown in a video
while neglecting the parts of the video that don't move
'''

#import numpy as np
import cv2
import imutils 

cap = cv2.VideoCapture('bakteria_growth.mp4')

# check success
if not cap.isOpened():
    raise Exception("Could not open video")

fgbg = cv2.createBackgroundSubtractorMOG2()

while(cap.isOpened()):
    
    # read picture, ret === True on success
    ret, frame = cap.read()
    
    # resize
    frame = imutils.resize(frame, width=600)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # apply mask
    fgmask = fgbg.apply(frame)
    
    # add circle as frame
    cv2.circle(frame, (310, 170), 150, (0, 0, 255), 3)
 
    # display windows
    cv2.imshow('fgmask',frame)
    cv2.imshow('frame',fgmask)

    # exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()