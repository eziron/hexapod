from servo_carteciano import Hexapod
import multiprocessing as mp
import numpy as np
import time
import json
import os

def print_var(Hexapod_dic):
    while(True):
        print(Hexapod_dic)
        time.sleep(0.5)

def read_var(Hexapod_dic):
    while(True):
        Hexapod_dic[0] = np.random.random()
        time.sleep(1)

with mp.Manager() as manager:
    Hexapod_dic = manager.list([0.0])

    p1 = mp.Process(target=print_var, args=(Hexapod_dic,))
    p2 = mp.Process(target=read_var, args=(Hexapod_dic,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()