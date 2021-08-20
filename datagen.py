import pandas as pd
import threading
import time
import concurrent.futures
import mathfunctions as mf
import numpy as np

class ThreadLock(object):
    def __init__(self):
        self.lock = threading.Lock()
    def addValues(self, values):
        self.lock.acquire()
        # print('lock')
        try:
            global bigframe
            bigframe = pd.concat((bigframe, values))
            bigframe.sort_index(inplace=True)
            bigframe.to_csv("numbers.csv")
        finally:
            self.lock.release()
            # print('unlock')

def createFrame():
    return pd.read_csv('numbers.csv', index_col=0)

def calcNumSteps(num):
    steps = 0
    osteps = 0
    esteps = 0
    while num > 1:
        if num % 2 == 0:
            num = num / 2
            esteps += 1
        else:
            num = 3*num + 1
            osteps += 1
        steps += 1
    return steps,osteps,esteps

def findStart(df):
    return df.index[-1]

def threadfun(start, threadnum, totalthreads, lock):
    global count
    global running
    global bigframe
    global iterations
    running = True
    threadtotal = 0
    threadcount = 1
    threadframe = pd.DataFrame(columns=['steps','osteps','esteps','odd','prime','exponote','primefactors','factors'])
    num = start + threadnum
    primefactors, expo = mf.findprimefactors(num)
    factors = mf.findfactors(num)
    x,y,z = calcNumSteps(num)
    threadframe.loc[num] = (x,y,z,num%2 == 1, len(factors) == 2, expo, set(primefactors), factors)
    while running:
        if threadcount != iterations:
            num += totalthreads
            primefactors,expo = mf.findprimefactors(num)
            factors = mf.findfactors(num)
            #,steps,osteps,esteps,odd,prime,exponote,primefactors,factors
            x, y, z = calcNumSteps(num)
            threadframe.loc[num] = (x,y,z,num%2 == 1, len(factors) == 2, expo, set(primefactors), factors)
            threadcount += 1
        else:
            lock.addValues(threadframe)
            threadframe = pd.DataFrame(columns=['steps','osteps','esteps','odd','prime','exponote','primefactors','factors'])
            threadcount = 0
            threadtotal += 1
            if threadtotal > count:
                count = threadtotal
    time.sleep(5)
    while threadtotal < count:
        if threadcount != iterations:
            num += totalthreads
            threadframe.loc[num] = calcNumSteps(num)
            threadcount += 1
        else:
            lock.addValues(threadframe)
            threadframe = pd.DataFrame(columns=['steps','osteps','esteps','odd','prime','exponote','primefactors','factors'],)
            threadcount = 0
            threadtotal += 1
if __name__ == "__main__":
    try:
        global count
        global running
        global bigframe
        global iterations
        iterations = 1000
        bigframe = createFrame()
        # print(frame)
        num = findStart(bigframe)+1
        # stop = 20
        running = True
        count = 0
        threads = 1
        locker = ThreadLock()

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            for i in range(threads):
                executor.submit(threadfun, num, i, threads, locker)
            input('Press enter to stop:')
            running = False




    except Exception as e:
        print(e)
        print('I made an oopsies please forgive me')



    finally:
        bigframe.sort_index(inplace=True)
        bigframe.to_csv('numbers.csv')

'''
Create global dataframe
Have each thread manipulate a separate dataframe
Every 1000? numbers append to global and save as csv
Place a lock on the global manipulation
Make sure the finish out a full rotation i.e. 1,2,3 not 1,3

Needs to never skip a number.
Would like to try for 8 threads. Maybe more?

Add Categories to DF:
Even
Odd
Factors
Prime
Exponential Notation (3^2=9, 5^1=5, 14^1=14)
'''