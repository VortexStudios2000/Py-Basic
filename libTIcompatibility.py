import time
import os
import math

def ClrHome():
    os.system("cls")

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