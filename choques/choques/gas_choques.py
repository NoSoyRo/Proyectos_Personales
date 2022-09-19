import numpy as np
import matplotlib.pyplot as plt 
from numpy import random as rand
from numpy import linalg as lng 

class p():
    def __init__(self, p_ini, v_ini, m, r):
        self.v = v_ini
        self.p = p_ini
        self.m = m
        self.r = r

def correccion_traslapes(Lista_De_Parts):
    for i in Lista_De_Parts:
        for j in Lista_De_Parts:
            if i != j:
                if lng.norm(i.p-j.p) < i.r+j.r :
                    gamma = i.r+j.r-lng.norm(i.p-j.p)
                    v = (i.p-j.p)/(lng.norm(i.p-j.p))
                    corr = gamma * v 
                    i.p = corr
                    print("hubo corrección")

def gen_n_parts(num_parts, lx, ly, vx, vy):
    
    masa, radio = 1,1   #<--- Esto lo puedo cambiar para que el usuario de las masas y radios.
    listax = np.linspace(-lx+radio,lx-radio,1000)
    listay = np.linspace(-ly+radio,ly-radio,1000)
    listavx = np.linspace(-vx,vx,1000)
    listavy = np.linspace(-vy,vy,1000)
    Particulas = []
    for i in range(num_parts):
        x,y = rand.choice(listax),rand.choice(listay)
        vx,vy = rand.choice(listavx),rand.choice(listavy)
        p_i_ini = np.array([x,y])
        v_i_ini = np.array([vx,vy])
        p_i = p(p_i_ini,v_i_ini,masa,radio)
        Particulas.append(p_i)
    correccion_traslapes(Particulas)
    return(Particulas)

L = gen_n_parts(3,2,2,2,2)
pos = []
for i in L:
    pos.append(i.p)
X = [i[0] for i in pos]
Y = [i[1] for i in pos]
plt.scatter(X,Y, s = 10)
plt.xlim(-2,2)
plt.ylim(-2,2)
plt.show()
    