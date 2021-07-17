from io import BytesIO
from time import sleep
from PIL import Image, ImageDraw, ImageFilter
from datetime import datetime, time
# import ctypes

from pynput import mouse
from pynput.mouse import Button, Controller

import utils as u
import pyscreenshot as ImageGrab
import numpy as np

import userInteraction as ui
# import downBarLoop as dbl
# import sys


# import pywinauto

# import win32con
# import win32com.client
# import win32api

import time


# datetime object containing current date and time
now = datetime.now()
userIndication = ui.getNextClickPos()
# sleep(2)
## - - - - -- - 
# jegododo =  [(2267, 800), (2299, 800), (2331, 800), (2363, 800),(2410, 800),(2395, 800),(2427, 800),(2459, 800)]
# grp = 200
# ind = 5
# dbl.handleNextFish( 14,  grp, ind  )
## - - - - - - -

## DIMS 
begX = userIndication[0] - 185
begY = userIndication[1] + 80
# - - - - 
endX = begX+100
endY = begY+100
# - - - - 
boxRangeX = endX - begX
boxRangeY = endY - begY
# - - - -
targetColor = (58, 92, 123) #metin2 average fish color - 19/11/20
#targetColor = (57,90,121)



def aLaPecheDeBonMatin():

    im = ImageGrab.grab(bbox=( begX, begY, endX, endY) , backend="mss", childprocess=False )  # X1,Y1,X2,Y2

    imData = u.getListOfPixelPosByColor( im, boxRangeX, boxRangeY, targetColor, 3 )
    #imData = u.getListOfPixelPosByColor( im, boxRangeX, boxRangeY, targetColor, 3 )
    
    if len(imData) == 0: 
        return 'pas de poisson dans la cible'
    else:
        beg = int((len( imData )/2)-5)
        end = int((len( imData )/2 )+5)

        droite = imData[beg:end]

        targ = droite[int(len(droite)/2)]
        targX = targ[0] + begX
        targY = targ[1] + begY


        #take mouse control
        mouse = Controller()
        mouse.position = (targX,targY)
        mouse.click( Button.left,1)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,targX,targY)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,targX,targY)

import keyboard  # using module keyboard

def startFishing():
    time.sleep(1.5)
    while True:
        if keyboard.is_pressed('y'):
            stopFishing()
            break

        res = aLaPecheDeBonMatin()

def stopFishing():
    time.sleep(1.5)
    while True:
        if keyboard.is_pressed('y'):
            startFishing()
            break

startFishing()
    

#im.save('img/metin_'+  now.strftime("%d%m%Y%H%M%S") +'.png')