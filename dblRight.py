import time
import utils as u
from pynput.mouse import Button, Controller


jegododo =  [(1135, 608), (1343, 609), (1343, 609), (1343, 609),(1343, 609),(1311, 609),(1343, 609),(1375, 609)]
grp = 201
ind = 7
    
def handleNextFish( interval, grp, ind ):

    u.moveThenClick( 'right' , jegododo[ind] )

    u.moveThenClick( 'right' ,(1482, 477))

    u.moveThenClick( 'right' , jegododo[0] )

    grp-=1
    if(ind==4):
        exit('1')           
    if(grp==0):
        grp=200
        ind-=1

    time.sleep( interval )
    handleNextFish( interval,  grp, ind  )


handleNextFish( 14,  grp, ind  )



