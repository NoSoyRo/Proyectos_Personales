import numpy as np
import matplotlib.pyplot as plt 
from numpy import random as rand
from numpy import linalg as lng 
from matplotlib.collections import EllipseCollection
RADIO=0.010
NPARTS=1000



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

def detector_traslapes(Lista_De_Parts, part_prueba):
    posis = np.array([])
    posc=part_prueba.p
    for i in Lista_De_Parts:
        if (lng.norm(i.p - posc) < i.r+part_prueba.r):
            print("colision detectada")
            return(True)

    return(False)

def gen_n_parts(num_parts, lx, ly, vx, vy):
    
    masa, radio = 1,RADIO   #<--- Esto lo puedo cambiar para que el usuario de las masas y radios.
    listax = np.linspace(-lx+radio,lx-radio,1000)
    listay = np.linspace(-ly+radio,ly-radio,1000)
    listavx = np.linspace(-vx,vx,1000)
    listavy = np.linspace(-vy,vy,1000)
    Particulas = []
    pos = []
    for i in range(num_parts):
        x,y = rand.choice(listax),rand.choice(listay)
        vx,vy = rand.choice(listavx),rand.choice(listavy)
        p_i_ini = np.array([x,y])
        v_i_ini = np.array([vx,vy])
        p_i = p(p_i_ini,v_i_ini,masa,radio)
        while(detector_traslapes(Particulas,p_i)):
            x,y = rand.choice(listax),rand.choice(listay)
            p_i_ini = np.array([x,y])
            p_i = p(p_i_ini,v_i_ini,masa,radio)
        

        
        Particulas.append(p_i)
        pos.append([x,y])
    return(Particulas)

def gen_proys(Lista_De_Parts,dt,n):
    espacio_proys=[]
    for i in Lista_De_Parts:
        posix = i.p[0]
        posiy = i.p[1]
        velix = i.v[0]
        veliy = i.v[1]

        espacio_proys.append([np.linspace(posix, posix+velix*dt,n),np.linspace(posiy, posix+veliy*dt,n),np.linspace(0, dt,n)])
    return espacio_proys

L = gen_n_parts(NPARTS,2,2,2,2)
pos = []
iter=0

plt.figure(figsize=[5, 5])

for i in L:
    pos.append([i.p[0],i.p[1]])
    circle1=plt.Circle((i.p[0], i.p[1]), RADIO, color=[0,0,0])
    plt.gcf().gca().add_artist(circle1)

#    circle=plt.Circle((posx[iter],posy[iter]),2)
#    iter += 1


plt.xlim(-2,2)
plt.ylim(-2,2)
plt.show()
gen_proys(L,0.5,10)    