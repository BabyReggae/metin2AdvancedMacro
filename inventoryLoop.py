import sys
import time
import utils as u
import keyboard
from pynput.mouse import Button, Controller


initFoodPos = [58, 702]
fishActionSlotPos = [896, 1030]
nbPerPack = 1
indX = 4
indY = 7 ### care , below const value ref on 7

# itemAreaType may be or '
def handleNextFish( 
    timeStep, 
    nbPerPack, 
    leftInPack, 
    nbSlotX, 
    nbSlotY, 
    fishFoodSlotPos, 
    fishActionSlotPos, 
    itemAreaType, 
    indX, 
    indY, 
    runing 
):
    # mouse = Controller()
    # mouse.position = (fishFoodSlotPos[0],fishFoodSlotPos[1])
    request = False

    if keyboard.is_pressed(''):

        break


    if(runing):
        u.moveThenClick( 'right' , fishFoodSlotPos )
        u.moveThenClick( 'right' , fishActionSlotPos )

        leftInPack-=1

        if(indX==0 and indY==0):
            exit('1')

        if(leftInPack==0 and indX == 0 ):
            indX = 4
            indY-=1
            fishFoodSlotPos[0] = 58
            fishFoodSlotPos[1] = 702 + ( 32 * (7-indY))
            leftInPack=nbPerPack

        elif(leftInPack==0):
            indX-=1
            fishFoodSlotPos[0] =  58 + ( 32 * (4-indX) )
            leftInPack=nbPerPack

        time.sleep( timeStep )
    else:
        time.sleep( 0.2 )
    handleNextFish( timeStep, nbPerPack, leftInPack, nbSlotX, nbSlotY, fishFoodSlotPos, fishActionSlotPos , itemAreaType, indX, indY  )

#handleNextFish( 14,  grp, ind  )
# def : coord = (x,y)
def moveByInterRecur( coord,  iterLeft):
    mouse = Controller()
    mouse.position = (coord[0],coord[1])
    time.sleep(0.8)
    coord[0]+=32

    coord[1]+=32
    iterLeft-=1
    if( iterLeft == 0 ):
        exit('fin du loop')
    moveByInterRecur(coord, iterLeft )

def moveThenClick( mouseBtn, coord ):
    mouse = Controller()
    time.sleep(0.1)
    mouse.position = (coord[0],coord[1])
    time.sleep(0.5)
    mouse.click( Button[mouseBtn],1)
    time.sleep(0.1)

handleNextFish( 14, 1, 1, 4, 6, initFoodPos, fishActionSlotPos , "none", indX, indY  )

