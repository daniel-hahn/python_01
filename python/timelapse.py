#!/usr/bin/python
# BEFORE USING THIS SCRIPT.
# mkdir ~/timelapse 
# mkdir ~/timelapse/completed
# this file should live in ~/timelapse and is run with command "python ~/timelapse/timelapse.py

import time
from picamera import PiCamera
from os import system
import RPi.GPIO as GPIO

# use GPIO.BOARD for enumerated pin numbers 
GPIO.setmode(GPIO.BCM)

# relay setup
GPIO.setup(21, GPIO.OUT)

# cam setup
camera = PiCamera()
camera.resolution = (1920, 1080)
# if camera is flipped and upside down - this fixes that
# camera.vflip = True
# camera.hflip = True

# timelapse setup
SleepTimeL = 10*60 # invall in sec
FrameCount = 0 # start number
FrameStop = 240 # number of total pics to take

WAIT = int(FrameStop)*int(SleepTimeL)/60

print('Photography will take approximately ' + str(WAIT) + ' minutes')
print('Taking photos now')

# take pics with flash
while (FrameCount < FrameStop):
    print('Picture:' + str(FrameCount) + ' of ' + str(FrameStop))
    print('turnig Relay ON')
    GPIO.output(21, GPIO.HIGH)
    time.sleep(1) # wait to turn on flash
    camera.capture('image' + str(FrameCount).zfill(4) + '.jpg') # 4: 9999 pics max
    print('turnig Relay OFF')
    GPIO.output(21, GPIO.LOW)
    time.sleep(SleepTimeL -1)
    FrameCount = FrameCount + 1

# create and move film
print('converting to film now')
system('ffmpeg -r 24 -i image%04d.jpg -vcodec libx264 -crf 20 -g 15 `date +%Y%m%d%H%M`timelapse.mp4')
print('moving to folder')
system('mv *.mp4 ~/timelapse/completed/')
# print('cleaning up old jpgs')
# system('rm *.jpg')
print('done')