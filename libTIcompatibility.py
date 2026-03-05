import time
import os
import subprocess
import math
from typing import Callable, List
import sys

def ClrHome():
    subprocess.call('cls' if os.name=='nt' else 'clear', shell=True)

def Output(row:int,col:int,text:str):
    print(text)

def Wait(dur:int):
    time.sleep(dur)

def Disp(value:int|float):
    print(value)

def Input(prompt:str) -> float:
    return float(input(prompt))

def Sqrt(num:int|float):
    return math.sqrt(num)

def Menu(prompt:str,labels:list[str],functions: List[Callable[[],None]]):
    print(prompt)
    num = len(labels)
    for i in range(num):
        print(f"{i} | {labels[i]}")
    response = int(input())
    func = functions[response]
    func()

def Pause(prompt:str):
    print(prompt)
    input()

def Stop():
    sys.exit()