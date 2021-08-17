# global count
# global running
# global list
import threading
import time
import concurrent.futures


class ThreadLock(object):
    def __init__(self):
        self.lock = threading.Lock()
    def addValues(self, values):
        self.lock.acquire()
        try:
            global mylist
            mylist.extend(values)
            # print(mylist)
        finally:
            self.lock.release()


def threadfun(start, threadnum, totalthreads, lock):
    global count
    global running
    global mylist
    global iterations
    threadtotal = 0
    threadcount = 1
    threadlist = [start+threadnum]
    num = start+threadnum
    while running:
        if threadcount != iterations:
            num += totalthreads
            threadlist.append(num)
            threadcount += 1
        else:
            lock.addValues(threadlist)
            threadlist = []
            threadcount = 0
            threadtotal += 1
            if threadtotal > count:
                count = threadtotal
    time.sleep(5)
    while threadtotal < count:
        if threadcount != iterations:
            num += totalthreads
            threadlist.append(num)
            threadcount += 1
        else:
            lock.addValues(threadlist)
            threadlist = []
            threadcount = 0
            threadtotal += 1

if __name__ == '__main__':
    global count
    global running
    global mylist
    global iterations
    count = 0
    iterations = 10
    running = True
    mylist = []
    locker = ThreadLock()

        # t = threading.Thread(target=threadfun, args=(0,i,8,locker))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for i in range(8):
            executor.submit(threadfun,0,i,8,locker)
        running = False
    # time.sleep(.5)
    # main_thread = threading.currentThread()


    mylist.sort()
    print(mylist)
    check = 0
    for x in mylist:
        if check != x:
            print('missing')
        check += 1