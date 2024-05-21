import utils as u
import userInteraction as ui
import os

import virtualKeyboardEvents as VK_event

import pyscreenshot as ImageGrab
import keyboard

from time import sleep
from datetime import datetime

from pynput.mouse import Button, Controller
from multiprocessing.pool import ThreadPool
import sys
from pygame import mixer  # Load the popular external library
#lol
mixer.init()
mixer.music.load('D:/Web_game_solo/metin2AdvancedMacro/mp3/ffx_victorySong.mp3')
clear = lambda: os.system('cls')
clear()

print ('Prix item a => :', '"'+str(sys.argv[2])+'$"'  )
print('edit test')

_FINISH = False
now = datetime.now()
print("Target the DragonStone's Slot")

userIndication = ui.getNextClickPos()
## ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def detectAncorGetMetinWindowPosition( ui, scanBoxRange ):
    now = datetime.now()
    half = int(scanBoxRange/2)

    im = ImageGrab.grab( bbox=( ui[0]-half, ui[1]-half, ui[0]+half, ui[1]+half), backend="mss",childprocess=False )  # X1,Y1,X2,Y2
    im.save("ancor/user_suggest.png")
    sleep(1)

    stoneInSuggestPos = u.getImgPosInImg('ancor/user_suggest.png' , 'ancor/dragonStone.png', debug=False )
    print(  stoneInSuggestPos )
    # incr by  ui imgPos
    metinWindowsX = ui[0]-half + stoneInSuggestPos[0] - 751
    metinWindowsY = ui[1]-half + stoneInSuggestPos[1] - 179

    if( stoneInSuggestPos == [0,0] ):
        exit('Ancor not found')

    
    return [metinWindowsX,metinWindowsY]

def updMetinWindowFrame( windowsPos, configWidth = 800, configHeight = 600 ):
    im = ImageGrab.grab( bbox=( windowsPos[0],  windowsPos[1],  windowsPos[0] + configWidth,  windowsPos[1] + configHeight), backend="mss",childprocess=False )  # X1,Y1,X2,Y2
    im.save("ancor/metin.png")
    sleep(0.1)

def initialize_shop( shopName = "default name"):
   
    # verif if shop packet present in inventory ?
    # attribute to downBarShortcut ?
    # press shortCut 
    VK_event.UseKey('F4')
    # Fill the Name
    VK_event.Write( shopName )
    # Press enter 
    VK_event.UseKey('Enter')

def getAbsolutBoardPosByAncor( ancor ):
    refs =  {
        "swapToPage1" : (-106,244),   #dist refAncor->SwapInventory <= 
        "invFirstSlot" : (638+10,250+10),#dist refAncor->FirstSlot
        "leftTopRedCircle" : (-569, -47), #refAncor-> fishAncor pool
        "prepareThrow" : (-161, -100),#refAncor-> prepareThrow
        "acceptThrow" : (-411,  138),#refAncor-> acceptThrow
        "shopPos" : (320,180),
        "acceptShop": ( 370, 360 ),
        "endShop" : ( 360, 460 )
    }   
    #init new array with defined properties
    res = refs
    #fill dat new arr
    res['invFirstSlot']      = ( ancor[0] + refs['invFirstSlot'][0], ancor[1]+refs['invFirstSlot'][1] )
    res['swapToPage1']       = ( ancor[0] + refs['swapToPage1'][0], ancor[1]+refs['swapToPage1'][1] )
    res['leftTopRedCircle']  = ( ancor[0] + refs['leftTopRedCircle'][0], ancor[1]+refs['leftTopRedCircle'][1] )
    res['prepareThrow']      = ( ancor[0] + refs['prepareThrow'][0], ancor[1]+refs['prepareThrow'][1] )
    res['acceptThrow']       = ( ancor[0] + refs['acceptThrow'][0], ancor[1]+refs['acceptThrow'][1] )
    res['shopPos']           = ( ancor[0] + refs['shopPos'][0], ancor[1]+refs['shopPos'][1] )
    res['acceptShop']        = ( ancor[0] + refs['acceptShop'][0], ancor[1]+refs['acceptShop'][1] )
    res['endShop']           = ( ancor[0] + refs['endShop'][0], ancor[1]+refs['endShop'][1] )

    return res

def getInventoryGrid( boardPos ):
    inv = {}
    for x in range(5):
        inv[x] = {}
        for y in range(9):
            inv[x][y] = { 'x' :  boardPos['invFirstSlot'][0]+(32*x), 'y' : boardPos['invFirstSlot'][1]+(32*y) } 

    return inv

def moveOverInventorySlots( slotSet ):
    for x in range(len(slotSet)):
        for y in range(len(slotSet[x])):
            u.moveTo(  slotSet[x][y] )
            sleep( 0.05 )

def inventorySnapShot( pos, inv ):
    for x in range(len(inv)):
        for y in range(len(inv[x])):
            im = ImageGrab.grab( bbox=( inv[x][y][0]-10, inv[x][y][1]-10, inv[x][y][0]+10, inv[x][y][1]+10 ), backend="mss",childprocess=False )  # X1,Y1,X2,Y2

            im.save('ancor/shoots/metin_'+ str(x) +'_'+ str(y) +'.png')
            # if( open("ancor/refs/bait1.png","rb").read() == open('ancor/shoots2/metin_'+ str(x) +'_'+ str(y) +'.png',"rb").read() ):
            #     return inv[x][y]

def getShopInventoryGrid( boardPos ):
    shopInvPos = u.getImgPosInImg( 'ancor/metin.png' , 'ancor/voidShop.png' )
    if shopInvPos == [0,0]:
        print('shop not found in metinWindow')
        return False

    inv = {}
    for x in range(5):
        inv[x] = {}
        for y in range(8):
            inv[x][y] = { 'x' :  boardPos['shopPos'][0]+(32*x) +15 , 'y' : boardPos['shopPos'][1]+(32*y) +15 } 

    return inv

def autoGlobal() :
    mainAncor = detectAncorGetMetinWindowPosition( userIndication , 100 )
    initialize_shop()
    updMetinWindowFrame( mainAncor )

    pos = getAbsolutBoardPosByAncor( mainAncor )
    inv = getInventoryGrid( pos )
    shop = getShopInventoryGrid(pos)


    mouse = Controller()
    mouse.position = (shop[0][0]['x'] , shop[0][0]['y'])
    iShop = 0
    for x in range(5):
        for y in range(8):
            u.moveToCoord(  inv[x][y] )
            sleep(0.2)
            nbTry = 0
            res = None
            while( nbTry < 4 ):
                res = u.getItemPriceByParsingMousePosImg( inv[x][y],debug=False, iter=nbTry )
                if res != None: break
                print( res, nbTry )
                nbTry+=1
                
            if res == None: 
                print('exited')

                exit(0)

            mouse = Controller()
            mouse.click( Button.left,1)

            shopX = iShop // 5 
            shopY = iShop % 5
            print( shopX , shopY )
            u.moveToCoord(  shop[shopX][shopY] )
            sleep(0.1)
            mouse.click( Button.left,1)
            sleep(0.1)
            VK_event.Write( str(res['default']['yang']), True )
            VK_event.UseKey( "Enter" )
            iShop+=1
            sleep(0.5)

def autoDoom( price, shopName ):
    mainAncor = detectAncorGetMetinWindowPosition( userIndication , 100 )
    initialize_shop( shopName )
    # The `updMetinWindowFrame` function takes the position of the Metin window frame as input and
    # captures a screenshot of the specified area within the Metin window. It saves this screenshot as
    # an image file named "metin.png" in the "ancor" directory. The function is used to update the
    # frame of the Metin window for further processing or analysis within the script.
    # The `updMetinWindowFrame` function takes the position of the Metin window frame and updates the
    # screenshot of the Metin window. It captures a new screenshot of the Metin window based on the
    # provided window position and saves it as "ancor/metin.png". This function is used to refresh the
    # image of the Metin window for further processing or analysis in the automation script.
    updMetinWindowFrame( mainAncor )

    pos = getAbsolutBoardPosByAncor( mainAncor )
    inv = getInventoryGrid( pos )
    shop = getShopInventoryGrid(pos)

    
    for x in range(1):
        for y in range(8):
            u.moveThenClickCoord( "left" , inv[x][y] )
            u.moveThenClickCoord( "left" , shop[x][y] )
            VK_event.Write( str(price), True )
            u.moveThenClick( "left" , pos["acceptShop"] )
    
    u.moveThenClick("left" , pos['endShop'])
    


method = str(sys.argv[1])
price = str(sys.argv[2])
name = str(sys.argv[3])

if method == "doom" and price != "" :
    if( name == "" or name == None ):
        name = None

    autoDoom( price , name )
    mixer.music.play()
    sleep(6)
else : 
    print("'You need to run command as => 'py autoShop.py [method] [price]'")
    print(  'EXAMPLE BELOW => \r\n py autoShop.py doom "150 000"')


# inv[4][2]['price'] = "10000"
# print( inv[4][2].get( 0 ) )
# VK_event.UseKey( "4" , True )
# VK_event.UseKey( "Enter" )
# 

# print( res )
# # mouse.click( Button.left,1)
# sleep(  3 )
# initialize_shop()


