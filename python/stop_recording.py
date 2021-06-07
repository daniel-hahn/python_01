import pyautogui
import time

#screenWidth:1280
#screenHeight: 800

stopRecX = 1006
stopRecY = 14

sleeptime = 105 #min

sleep(sleeptime*60) #sec
pyautogui.click(stopRecX, stopRecY)
#pyautogui.click('button.png')
#pyautogui.moveTo(stopRecX, stopRecY)
