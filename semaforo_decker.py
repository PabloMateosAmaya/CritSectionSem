from multiprocessing import Process
from multiprocessing import current_process
from multiprocessing import Value, Array
from multiprocessing import BoundedSemaphore
import time
import random
N = 8
sem=BoundedSemaphore(1)
'''def is_anybody_inside(critical, tid):
    found = False
    i = 0
    while i<len(critical) and not found:
        found = tid!=i and critical[i]==1
        i += 1
    return found'''

def task(common, tid, critical, turn):
    a = 0
    for i in range(20):
        print(f'{tid}−{i}: Non−critical Section',flush=True)
        a += 1
        print(f'{tid}−{i}: End of non−critical Section',flush=True)
        time.sleep(random.random())
        critical[tid] = 1
        sem.acquire()
        print(f'{tid}−{i}: Critical section',flush=True)
        v = common.value + 1
        print(f'{tid}−{i}: Inside critical section',flush=True)
        time.sleep(random.random())
        common.value = v
        print(f'{tid}−{i}: End of critical section',flush=True)
        sem.release()
        critical[tid] = 0
        turn.value = tid
def main():
    lp = []
    common = Value('i', 0)
    critical = Array('i', [0]*N)
    turn = Value('i', 0)
    for tid in range(N):
        lp.append(Process(target=task, args=(common, tid, critical, turn)))
    print (f"Valor inicial del contador {common.value}")
    for p in lp:
        p.start()
    for p in lp:
        p.join()
        
    print (f"Valor final del contador {common.value}")
    print ("fin")

if __name__ == "__main__":
    main()