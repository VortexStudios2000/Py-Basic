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
    Output(5,7,"PHYSICS UNITS")
    Menu("Pick a Topic",["Kinematics","Forces","Circular Motion","Energy/Work","QUIT"],[A1,A2,A3,A4,Q0])

def A1():
    Menu("",["Position - x/y (m)","Velocity - v (m/s)","acceleration - a (m/s^2)","BACK"],[A1,A1,A1,A0])
    Stop()

def A2():
    Menu("",["Force - N (kg*m/s^2)","Mass - kg","BACK"],[A2,A2,A0])
    Stop()
def A3():
    Menu("",["a_c (m/s^2)","F_c (N)","lowercase omega (rad/s)","Period - T (s)","Frequency-f(Hz=cycles/s)","BACK"],[A3,A3,A3,A3,A3,A0])
    Stop()
def A4():
    Menu("",["Work - W (J=kgm^2/s^2)","Kinetic Energy - KE (J)","Potential Energy - U (J)","BACK"],[A4,A4,A4,A0])
    Stop()

def Q0():
    Stop()

# __init__ #

A0()