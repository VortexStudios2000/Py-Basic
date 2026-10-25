from libTIcompatibility import *

a:float=0
b:float=0
c:float=0
d:float=0
e:float=0
f:float=0
g:float=0
h:float=0
i:float=0
j:float=0
k:float=0
l:float=0
m:float=0
n:float=0
o:float=0
p:float=0
q:float=0
r:float=0
s:float=0
t:float=0
u:float=0
v:float=0
w:float=0
x:float=0
y:float=0
z:float=0
θ:float=0

# __start__ #

def A0():
    ClrHome()
    Output(5,7,"STARTING UP...")
    Wait(1)
    ClrHome()
    Menu("Choose",["Pythagorean Theorem","Cone Volume","Sphere Volume"],[A1,A2,A3])

def A1():
    ClrHome()
    print("Pythagorean Theorem")
    a = float(input("leg1 = "))
    b = Input("leg2 = ")
    c=(a**2+b**2)**.5
    a=0
    b = 0
    print("Hypotenuse = ",c)
    Pause("Press enter to continue...")
    Stop()

def A2():
    ClrHome()
    print("Volume of a Cone")
    print("V=1/3*πhr^2")
    r = Input("r = ")
    h = Input("h = ")
    v = 1/3*PI*h*r**2
    r=0
    h=0
    print("Volume = ",v)
    Pause("Press enter to continue...")
    Stop()

def A3():
    ClrHome()
    print("Volume of a Sphere")
    print("V=4/3*πr^3")
    r = Input("r = ")
    v = 4/3*PI*r**3
    r=0
    print("Volume = ",v)
    Pause("Press enter to continue...")
    Stop()

# __init__ #

A0()
