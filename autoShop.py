import utils as u
import time
import keyboard

leun = (109, 737)
ledeux = ( 149, 737 )
letrois = (186, 734)
lecinq = (280, 737)
leneuf = (430, 730)
lezero = (437, 737)
enter = (608, 820)
invlefttoppos = (652, 287)
shoplefttoppos = (336, 223)

# for x in range( 5 ):
#     for y in range ( 8 ):
        
#         if keyboard.is_pressed('y'):
#             print('MANUAL STOP')
#             exit(1)
        
        
#         xPosInv =  (32 * x) + invlefttoppos[0]
#         yPosInv =  (32 * y) + invlefttoppos[1]
#         xPosShop =  (32 * x) + shoplefttoppos[0]
#         yPosShop =  (32 * y) + shoplefttoppos[1]
        
#         u.moveThenClick( 'left' ,  ( xPosInv , yPosInv ) )
#         time.sleep(0.8)
#         u.moveThenClick( 'left' ,  ( xPosShop  ,yPosShop ) )
#         time.sleep(0.8)
#         u.moveThenClick( 'left' ,  letrois )
#         u.moveThenClick( 'left' ,  lecinq )
        
#         for i in range( 5 ):
#             u.moveThenClick( 'left' ,  lezero )
            
#         u.moveThenClick( 'left' ,  enter )
            

for x in range( 5 ):
    for y in range ( 8 ):
        
        if keyboard.is_pressed('y'):
            print('MANUAL STOP')
            exit(1)
        
        
        xPosInv =  (32 * x) + invlefttoppos[0]
        yPosInv =  (32 * y) + invlefttoppos[1]
        xPosShop =  (32 * x) + shoplefttoppos[0]
        yPosShop =  (32 * y) + shoplefttoppos[1]
        
        u.moveThenClick( 'left' ,  ( xPosInv , yPosInv ) )
        time.sleep(0.8)
        u.moveThenClick( 'left' ,  ( xPosShop  ,yPosShop ) )
        time.sleep(0.8)
        # u.moveThenClick( 'left' ,  letrois )
        u.moveThenClick( 'left' ,  leun )
        
        for i in range( 6 ):
            u.moveThenClick( 'left' ,  leneuf )
            
        u.moveThenClick( 'left' ,  enter )
