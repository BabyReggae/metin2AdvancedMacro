import time
import utils as u
from pynput.mouse import Button, Controller


jegododo =  [(330, 609), (362, 609), (394, 609), (426, 609),(468, 609),(500, 609),(532, 609),(564,609)]
#jegododo =  [(2529, 798), (362, 609), (394, 609), (426, 609),(468, 609),(500, 609),(532, 609),(2763, 799)]
grp = 201
ind = 7

def handleNextFish( interval, grp, ind ):

    u.moveThenClick( 'right' , jegododo[ind] )

    #u.moveThenClick( 'right' , (711, 481) )

    u.moveThenClick( 'right' , jegododo[0] )

    grp-=1
    if(ind==0):
        exit('1')           
    if(grp==0):
        grp=200
        ind-=1

    time.sleep( interval )
    handleNextFish( interval,  grp, ind  )


handleNextFish( 14,  grp, ind  )



