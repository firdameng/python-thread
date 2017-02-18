
# -*- coding: utf-8 -*-
from atexit import register
from random import randrange
from threading import BoundedSemaphore,Lock,Thread
from time import sleep,ctime

lock=Lock()   #互斥锁
MAX=5
candytray=BoundedSemaphore(MAX)

def refill():
    with lock:
        print 'refilling candy...'
        try:
            candytray.release()
        except ValueError:
            print 'full,skipping'
        else:
            print 'OK'
 
def buy():
    with lock:
        print 'buying candy....'
        if candytray.acquire(False):    #让调用不阻塞？？？
            print 'OK'
        else:
            print 'empty,skipping'
            
def producer(loops):
    for i in xrange(loops):
        refill()
        sleep(randrange(3))
        
def consumer(loops):
    for i in xrange(loops):
        buy()
        sleep(randrange(3))
def main():
    print 'starting at:',ctime()
    nloops=randrange(2,6)
    print 'the candy machine (full with %d bars)'%MAX
    Thread(target=consumer,args=(randrange(
    nloops,nloops+MAX+2),)).start()
    Thread(target=producer,args=(nloops,)).start()
 
@register
def _atexit():
    print 'all done at:',ctime()
if __name__=='__main__':
    main()