#多进程
import os
import threading
from multiprocessing import Pool

def f(x):
    pid = os.getpid()
    tid = threading.get_ident()
    print(pid, tid, x)

if __name__ == '__main__':

    pool = Pool(4)
    pool.map(f, [i for i in range(1, 11)])
    pool.close()
    pool.join()


#多线程
import os
import threading
from multiprocessing.dummy import Pool as threadPool

def f(x):
    pid = os.getpid()
    tid = threading.get_ident()
    print(pid, tid, x)

if __name__ == '__main__':
    tpool = threadPool(4)
    for i in range(1, 11):
        tpool.apply_async(f, args=[i])
    tpool.close()
    tpool.join()


#协程
import os
import threading
import asyncio

async def f(x):
    pid = os.getpid()
    tid = threading.get_ident()
    print(pid, tid, x)

async def main():
    await asyncio.gather(*[f(i) for i in range(1, 11)])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
