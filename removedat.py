# import time
# from multiprocessing.pool import ThreadPool
# from multiprocessing import Queue

# _FINISH = False


# def hang( int1 , int2, queue ):
#     while True:
#         if _FINISH:
#             break
#         print('action th1...' )

        
#         time.sleep(3)

# def hing(nbIter,queue):
#         if _FINISH:
#                 print('everything has an end')
#                 return
#         print('action th2... ')
#         time.sleep(1)
#         nbIter += 1
#         if( nbIter > 15 ):
#                 queue.put('hi darling')
#         hing(nbIter,queue)


# def main():
#         global _FINISH
#         queue  = Queue()

#         pool1 = ThreadPool(processes=1)
#         pool2 = ThreadPool(processes=2)
#         pool1.apply_async(hang ,args=(12 , 19, queue))
#         pool2.apply_async(hing, args=( 1,queue ))
#         time.sleep(5)

#         ### en gros ,n si ce queue.get() renvoie un 'finishing' on stop les deux thread , on lance le trieur , puis a la fin du trieur, on rappel main() ....
#         print('gonna wait for changes :p' , queue.qsize() )
#         while( True ):
#                 print( queue.qsize() , 'changes ?' )
#                 time.sleep( 1 )
#                 print('waiting for changes :p')
#                 if ("hi darling" !=  queue.get() ):
#                         break
                
#         _FINISH = True
#         pool1.terminate()
#         pool2.terminate()

#         pool1.join()
#         pool2.join()


#         # print("QUEUE => ", queue.qsize() , queue.get() )
#         # if( queue.get() == 'hi darling' ):


#         while not queue.empty():
#                 print(queue.get())

#         print('main process exiting..')


# if __name__ == '__main__':
#     main()

import time
_FINISH = False

def foo(bar, baz , ctn):
        time.sleep( 2 )
        print ('hello {0}'.format(bar) )
        ctn += 1
        if( ctn > 4 ):
                return 'foo' + baz
        else:
                foo( bar, baz , ctn )
        


def infinite(ctn=0):
        global _FINISH
        print('loop' , ctn )
        if _FINISH :
                print('value returned ! ')
                return( 'u did it dude :p')
        time.sleep(1)
        ctn += 1
        if( ctn > 20 ):
                return False
        infinite(ctn)
  
  
  

from multiprocessing.pool import ThreadPool

pool = ThreadPool(processes=1)
pool2 = ThreadPool(processes=2)

async_result = pool.apply_async(foo, ('world', 'foo' , 0)) # tuple of args for foo
stopdude = pool2.apply_async(infinite)  # tuple of args for foo

# do some other stuff in the main process


return_val = async_result.get() 
_FINISH = True

print('finish > ' , _FINISH )
time.sleep(1)
grale = stopdude.get()
print( grale  )

