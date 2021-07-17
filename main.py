import utils as u
import userInteraction as ui

import pyscreenshot as ImageGrab
import keyboard

from time import sleep
from datetime import datetime

from pynput.mouse import Button, Controller
from multiprocessing.pool import ThreadPool

_FINISH = False
now = datetime.now()
print("Target the DragonStone's Slot")
userIndication = ui.getNextClickPos()
## ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def detectAncorGetPosition( ui, scanBoxRange ):
    now = datetime.now()
    half = int(scanBoxRange/2)

    im = ImageGrab.grab( bbox=( ui[0]-half, ui[1]-half, ui[0]+half, ui[1]+half), backend="mss",childprocess=False )  # X1,Y1,X2,Y2
    #im.save('ancor/metin_'+  now.strftime("%d%m%Y%H%M%S") +'.png') -- (119,232,254)web
    res = u.findFirstPixePosInImgOnColor( im, scanBoxRange , scanBoxRange ,  (115,231,255) ) 
    if( res == None ):
        im.save('ancor/notFound/metin_'+  now.strftime("%d%m%Y%H%M%S") +'.png')
        exit('Ancor not found :s')

    res = ( res[0]- half , res[1]- half )
    mainAncor = ( ui[0] + res[0] , ui[1] + res[1]  )

    return mainAncor

def getAbsolutBoardPosByAncor( ancor ):
    refs =  {
        "swapToPage1" : (-106,46),   #dist refAncor->SwapInventory <= 
        "invFirstSlot" : (-110,74),#dist refAncor->FirstSlot
        "F4" : (-190, 396), #refAncor-> F4 
        "1" : (-428, 396), #refAncor-> 1 (fishing action slot ) 
        "leftTopRedCircle" : (-569, -47), #refAncor-> fishAncor pool
        "prepareThrow" : (-161, -100),#refAncor-> prepareThrow
        "acceptThrow" : (-411,  138),#refAncor-> acceptThrow
    }   

    res = refs
    res['invFirstSlot']      = ( ancor[0] + refs['invFirstSlot'][0], ancor[1]+refs['invFirstSlot'][1] )
    res['swapToPage1']       = ( ancor[0] + refs['swapToPage1'][0], ancor[1]+refs['swapToPage1'][1] )
    res['F4']                = ( ancor[0] + refs['F4'][0], ancor[1]+refs['F4'][1] )
    res['1']                 = ( ancor[0] + refs['1'][0], ancor[1]+refs['1'][1] )
    res['leftTopRedCircle']  = ( ancor[0] + refs['leftTopRedCircle'][0], ancor[1]+refs['leftTopRedCircle'][1] )
    res['prepareThrow']      = ( ancor[0] + refs['prepareThrow'][0], ancor[1]+refs['prepareThrow'][1] )
    res['acceptThrow']       = ( ancor[0] + refs['acceptThrow'][0], ancor[1]+refs['acceptThrow'][1] )

    return res

def setInventoryGrid( boardPos ):
    inv = {}
    for x in range(5):
        inv[x] = {}
        for y in range(9):
            inv[x][y] = ( boardPos['invFirstSlot'][0]+(32*x), boardPos['invFirstSlot'][1]+(32*y) ) 

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

mainAncor = detectAncorGetPosition( userIndication , 100 )
pos = getAbsolutBoardPosByAncor( mainAncor )
inv = setInventoryGrid( pos )

boxRange = 100
begX = pos['leftTopRedCircle'][0]
begY = pos['leftTopRedCircle'][1]
# - - - - 
endX = begX+boxRange
endY = begY+boxRange
# - - - - 
boxRangeX = endX - begX # c complétement con.... -_()
boxRangeY = endY - begY
# - - - -
targetColor = (58, 92, 123)

def aLaPecheDeBonMatin():
    global _FINISH
    def run():
        img = ImageGrab.grab(bbox=( begX, begY, endX, endY) , backend="mss", childprocess=False )  # X1,Y1,X2,Y2
        # im.save('ancor/notFound/metin_'+  now.strftime("%d%m%Y%H%M%S") +'.png')
        # exit(1)
        imgData = u.getListOfPixelPosByColor( img, boxRangeX, boxRangeY, targetColor, 3 )

        if len(imgData) == 0: 
            return
        else:
            beg = int((len( imgData )/2)-5)
            end = int((len( imgData )/2 )+5)

            droite = imgData[beg:end]

            targ = droite[int(len(droite)/2)]
            targX = targ[0] + begX
            targY = targ[1] + begY

            mouse = Controller()
            mouse.position = (targX,targY)
            mouse.click( Button.left,1)
    
    while( _FINISH == False):
        if keyboard.is_pressed('y'):
            _FINISH = True
        res = run()

    return 

def countVoidSlot(pos, inv):
    inventorySnapShot(pos, inv)
    voidSlot = open("ancor/refs/void.png","rb").read()
    ctn=0
    for x in range(len(inv)):
        for y in range(len(inv[0])):
            if( voidSlot == open('ancor/shoots/metin_'+ str(x) +'_'+ str(y) +'.png',"rb").read() ):
                ctn+=1
                continue
    
    return ctn

def getUnVoidSlotPos( inv ):
    inventorySnapShot(pos, inv)
    res = []
    nbVoidSlot = 0

    for x in range(len(inv)):
        res.append( [] )
        for y in range(len(inv[x])):
            auditedSlot =   open('ancor/shoots/metin_'+ str(x) +'_'+ str(y) +'.png',"rb").read()
            if( open("ancor/refs/void.png","rb").read() != auditedSlot ):
                nbVoidSlot += 1
                res[x].append( inv[x][y] )
    print( "\r\n" + str( nbVoidSlot ) + " slots utilisés ont été trouvé dans l'inventaire" )
    return res

## ///////////////////////////LOCAL SETTINGS //////////////////////////////////////////////////////////// 
jegododo =  [(330, 609), (362, 609), (394, 609), (426, 609),(468, 609),(500, 609),(532, 609),(564,609)]
_grp = 200
_ind = 7

def handleNextFish(interval):
    global _grp, _ind



    inventorySnapShot(pos, inv)
    left = countVoidSlot(pos,inv)
    if(left < 2 ):
        print('SCRIPT STOP')
        return True
    # else:   
    #     print('il reste '+ str(left)+' place')

    curBaitSlot = (  pos["F4"][0] - (( 7 - _ind )*32) ,  pos["F4"][1] )
    u.moveThenClick( 'right' , curBaitSlot )
    u.moveThenClick( 'right' , pos["1"] )

    _grp-=1
    if(_ind==0):
        exit('1')
    if(_grp==0):
        _grp=200
        _ind-=1

    msgPrint = "Il reste (normalement) " + str( _grp ) +" appat dans le pack"
    print (msgPrint, end="\r")
    
    delay = 0
    while( delay < interval ):
        if keyboard.is_pressed('y'):
            print('\r\nARRET DEMANDER')
            return True
        delay += 1
        sleep(1)
    
    # sleep( interval )
    handleNextFish( interval )

def moveByInterRecur( coord,  iterLeft):
    mouse = Controller()
    mouse.position = (coord[0],coord[1])
    sleep(0.8)
    coord[0]+=32

    coord[1]+=32
    iterLeft-=1
    if( iterLeft == 0 ):
        exit('fin du loop')
    moveByInterRecur(coord, iterLeft )

def startFishing():
    global _FINISH
    print('\r\ninitialisation : ')
    sleep(1.5)
    _FINISH = False
    print('prêt')
    print('\r\nappuyer sur "y/Y" pour stopper\r\n')
    

    pool = ThreadPool(processes=1)
    pool2 = ThreadPool(processes=2)

    handle = pool.apply_async(handleNextFish, ( 14, )) # NOTE extra ' , '  
    detector = pool2.apply_async(aLaPecheDeBonMatin) 

    return_val = handle.get() 
    _FINISH = True
    grale = detector.get()
    
    print( return_val ,grale )

    if keyboard.is_pressed('y'):
        print('FIN DU PROGRAMME')
        return


    startSortingLoop()

def startSortingLoop():
    global _FINISH

    restrictedSet = getUnVoidSlotPos(inv )
    moveOverInventorySlots( restrictedSet )
    # ensure no tooltip is over inventory before screen it
    u.moveTo( pos['prepareThrow'] )
    inventorySnapShot(pos, inv)
    print( "Début de l'analyse des slots utilisés : \r\n" )
    nbTrowable = nbUsable = nbNoActionRequired = 0


    for x in range(len(inv)):
        for y in range(len(inv[0])):
            auditedSlot =   open('ancor/shoots/metin_'+ str(x) +'_'+ str(y) +'.png',"rb").read()
            # print( x,y, "start audit V" )
            if( open("ancor/refs/void.png","rb").read() == auditedSlot ):
                continue
            # print( x,y, "not void" )

            _FINISH = False
            # if( open("ancor/refs/use/bait1.png","rb").read() == auditedSlot or open("ancor/refs/use/bait2.png","rb").read() == auditedSlot ):
            #     u.moveThenClick( 'right' , inv[x][y] )
            #     u.moveThenClick( 'right' , pos["1"] )
            #     print( 'detector on ' )
            #     pool = ThreadPool(processes=1)
            #     detector = pool.apply_async(aLaPecheDeBonMatin)  # tuple of args for foo
            #     print( 'resume in 13sec...' )
            #     sleep(13)
            #     _FINISH = True
            #     print('detector off')
            #     continue

            # print( x,y, "not a bait" )

            stackables = u.listFile( "ancor/refs/stack/" )
            for stk in range(len(stackables)):
                if( open( stackables[stk] ,"rb").read() == auditedSlot ):
                    u.moveThenClick( 'right' , inv[x][y] )
                    nbUsable += 1
                    continue
            
            # print( x,y, "not throwable" )

            throwables = u.listFile( "ancor/refs/throw/" )
            for thw in range(len(throwables)):
                if( open( throwables[thw] ,"rb").read() == auditedSlot ):
                    u.moveThenClick( 'left' , inv[x][y] )
                    u.moveThenClick( 'left' , pos['prepareThrow'] )
                    u.moveThenClick( 'left' , pos['acceptThrow'])
                    sleep(0.6)  # min 0.7
                    nbTrowable += 1
                    continue


            nbNoActionRequired += 1
    

    # print( str( nbNoActionRequired ) + " ne néccessitent aucune action" )
    print( str( nbTrowable ) + " ont été jétés" )
    print( str( nbUsable )+ " ont été utilisés" )

    inventorySnapShot(pos, inv)
    left = countVoidSlot(pos,inv)
    if(left < 2 ):
        nana = pos['swapToPage1']
        verif = ( nana[0]+42 , nana[1] )
        u.moveThenClick('left' , verif)
        print('change inventory page')

    # else:   
    #     print('il reste '+ str(left)+' place')
    
    
    # for i in range(5):
    #     if( i != 4 ):
    #         u.moveThenClick( 'left' , inv[4-i][8] )
    #         u.moveThenClick( 'left' , inv[3-i][8] )
    #### stack appat


    startFishing()
            # if( open("ancor/refs/bait1.png","rb").read() == open('ancor/shoots2/metin_'+ str(x) +'_'+ str(y) +'.png',"rb").read() ):
            #     return inv[x][y]

## __main__

startSortingLoop()
