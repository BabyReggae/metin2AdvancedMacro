# # from          e import Button, Controller

# # mouse = Controller()

# # # Read pointer position
# # print('The current pointer position is {0}'.format(
# #     mouse.position))

# # # Set pointer position
# # mouse.position = (10, 20)
# # # print('Now we have moved it to {0}'.format(
# # #     mouse.position))

# # # # Move pointer relative to current position
# # # mouse.move(5, -5)

# # # # Press and release
# # # mouse.press(Button.left)
# # # mouse.release(Button.left)

# # # # Double click; this is different from pressing and releasing
# # # # twice on macOS
# # # mouse.click(Button.left, 2)

# # # # Scroll two steps down
# # # mouse.scroll(0, 2)


# # ## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # ## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# # from time import sleep
# # # print('coucou')

# # def direbonjourLoop( loopInterval ):
# #     print('bonjour')
# #     sleep( loopInterval )


# # direbonjourLoop( 1 )

# def isPixelColorContainedInRange( begRangeRGB , endRangeRGB, auditedRGB ):
#     isContained = True
#     for ind in range(3):
#         if( auditedRGB[ind] < begRangeRGB[ind] or auditedRGB[ind] > endRangeRGB[ind] ):
#             return False

#     return isContained

# for ind in range( 10 ):
#     if (ind % 1000 == 0):
#         print('ran' , ind)
#     res = isPixelColorContainedInRange( (50,50,50) , (150,150,150), (49,130,140) )

# print( res )

# imanotlist = (10,10,10)

# new_list = [x+10 for x in imanotlist]
# from pynput.mouse import Listener

# def on_move(x, y):
#     print('Pointer moved to {0}'.format((x, y)))

# def on_click(x, y, button, pressed):
#     print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
#     if not pressed:
#         # Stop listener
#         return False

#     return (x,y)

# def on_scroll(x, y, dx, dy):
#     print('Scrolled {0}'.format((x, y)))

# # Collect events until released
# with Listener(on_click=on_click) as listener:
#     listener.join()





# from PIL import Image
# img = Image.open('ancor/marqueur.PNG')
# img.putalpha(128)  # Half alpha; alpha argument must be an int
# img.save('ancor/marqueurTrans.png')

# import win32api
# import time
# import win32gui
# import win32con
# import ctypes


# hold = win32gui.LoadImage(0, 32512, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED )
# hsave = ctypes.windll.user32.CopyImage(hold, win32con.IMAGE_CURSOR,0, 0, win32con.LR_COPYFROMRESOURCE)




# hnew = win32gui.LoadImage(0, 'ancor/marqueurTrans.cur', win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
# ctypes.windll.user32.SetSystemCursor(hnew, 32512)
# time.sleep(10)
# #restore the old cursor
# ctypes.windll.user32.SetSystemCursor(hsave, 32512)

# import win32api
# import win32con
# from ctypes import *
# import time

# # https://msdn.microsoft.com/en-us/library/windows/desktop/ms648395(v=vs.85).aspx
# SetSystemCursor = windll.user32.SetSystemCursor #reference to function
# SetSystemCursor.restype = c_int #return
# SetSystemCursor.argtype = [c_int, c_int] #arguments
# # https://msdn.microsoft.com/en-us/library/windows/desktop/ms648391(v=vs.85).aspx
# hCursor = win32api.LoadCursor( 0, win32con.OCR_APPSTARTING ) 

# if SetSystemCursor(hCursor, win32con.OCR_NORMAL) == 0:
#     print ("Error in setting the cursor")

# time.sleep(10)

# if SetSystemCursor(hCursor, win32con.OCR_NORMAL) == 0:
#     print ("Error in revert the cursor")

# from time import sleep
# import utils as u
# import pyscreenshot as ImageGrab
# import userInteraction as ui
# from datetime import datetime, time

# now = datetime.now()
# userIndication = ui.getNextClickPos()

# def detectAncorGetPosition( ui, scanBoxRange ):
#     now = datetime.now()
#     half = int(scanBoxRange/2)

#     im = ImageGrab.grab( bbox=( ui[0]-half, ui[1]-half, ui[0]+half, ui[1]+half), backend="mss",childprocess=False )  # X1,Y1,X2,Y2
#     #im.save('ancor/metin_'+  now.strftime("%d%m%Y%H%M%S") +'.png') -- (119,232,254)web
#     res = u.findFirstPixePosInImgOnColor( im, scanBoxRange , scanBoxRange ,  (115,231,255) ) 
#     if( res == None ):
#         im.save('ancor/notFound/metin_'+  now.strftime("%d%m%Y%H%M%S") +'.png')
#         exit('Ancor not found :s')

#     res = ( res[0]- half , res[1]- half )
#     mainAncor = ( ui[0] + res[0] , ui[1] + res[1]  )

#     return mainAncor

# def getAbsolutBoardPosByAncor( ancor ):
#     refs =  {
#         "swapToPage1" : (-106,46),   #dist refAncor->SwapInventory <= 
#         "invFirstSlot" : (-110,74),#dist refAncor->FirstSlot
#         "F4" : (-190, 396), #refAncor-> F4 
#         "1" : (-428, 396), #refAncor-> 1 (fishing action slot ) 
#         "leftTopPool" : (-384,-127), #refAncor-> fishAncor pool
#     }   

#     res = refs
#     res['invFirstSlot'] = ( ancor[0] + refs['invFirstSlot'][0], ancor[1]+refs['invFirstSlot'][1] )
#     res['swapToPage1']  = ( ancor[0] + refs['swapToPage1'][0], ancor[1]+refs['swapToPage1'][1] )
#     res['F4']           = ( ancor[0] + refs['F4'][0], ancor[1]+refs['F4'][1] )
#     res['1']            = ( ancor[0] + refs['1'][0], ancor[1]+refs['1'][1] )
#     res['leftTopPool']  = ( ancor[0] + refs['leftTopPool'][0], ancor[1]+refs['leftTopPool'][1] )

#     return res

# def setInventoryGrid( boardPos ):
#     inv = {}
#     for x in range(5):
#         inv[x] = {}
#         for y in range(9):
#             inv[x][y] = ( boardPos['invFirstSlot'][0]+(32*x), boardPos['invFirstSlot'][1]+(32*y) ) 

#     return inv

# def moveOverInventorySlots( inv ):
#     for x in range(len(inv)):
#         for y in range(len(inv[0])):
#             u.moveTo(  inv[x][y] )
#             sleep( 0.3 )

# def photoShooting( pos, inv ):
#     for x in range(len(inv)):
#         for y in range(len(inv[0])):
#             im = ImageGrab.grab( bbox=( inv[x][y][0]-10, inv[x][y][1]-10, inv[x][y][0]+10, inv[x][y][1]+10 ), backend="mss",childprocess=False )  # X1,Y1,X2,Y2
#             # im.save('ancor/shoots/metin_'+  now.strftime("%d%m%Y%H%M%S") +'.png')
#             im.save('ancor/shoots2/metin_'+ str(x) +'_'+ str(y) +'.png')
#             # if( open("ancor/refs/bait1.png","rb").read() == open('ancor/shoots2/metin_'+ str(x) +'_'+ str(y) +'.png',"rb").read() ):
#             #     return inv[x][y]


# mainAncor = detectAncorGetPosition( userIndication , 100 )
# pos = getAbsolutBoardPosByAncor( mainAncor )
# inv = setInventoryGrid( pos )
# #moveOverInventorySlots( inv )
# photoShooting( pos, inv )

# throwables = u.listFile( "ancor/refs/throw/" )
# for thw in range(len(stackables)):
#     if( open( throwables[thw] ,"rb").read() == auditedSlot ):
#         u.moveThenClick( 'left' , inv[x][y] )
#         u.moveThenClick( 'left' , pos['prepareThrow'] )
#         u.moveThenClick( 'left' , pos['acceptThrow'])
#         continue

# # for key in inv:
#     print( inv[key] )

# u.moveThenClick( 'right' , pos["swapToPage1"] )
# u.moveThenClick( 'right' , pos["invFirstSlot"] )
# u.moveThenClick( 'right' , pos["F4"] )
# u.moveThenClick( 'right' , pos["1"] )
# print( pos )





# #print( u.getNextClickPos() )

# x = 3
# y = 7

# print(open('ancor/shoots/metin_'+ str(x) +'_'+ str(y) +'.png' ,"rb").read() == open('ancor/refs/use/bait1.png' ,"rb").read())


# truc = False
import utils as u

print(u.getNextClickPos() )
