import time
import os

def ClrHome():
    os.system("cls")

def Output(row:int,col:int,text:str):
    print(text)

def Wait(dur:int):
    time.sleep(dur)