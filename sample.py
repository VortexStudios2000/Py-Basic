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

ClrHome()
Output(5,7,"STARTING UP...")
Wait(1)
ClrHome()
Output(5,8,"PY-BASIC 1.0")
a = Input("leg1 = ")
b = Input("leg2 = ")
c=Sqrt(a**2+b**2)
print("Hypotenuse = ",c)