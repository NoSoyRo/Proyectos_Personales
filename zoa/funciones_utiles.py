import numpy as np
from numpy import random as rand
import matplotlib.pyplot as plt

def movimiento_oveja(oveja):
    #el movimeinto de la oveja consiste en moverse velocidad*vector director para el vector director necesito un angulo
    #theta entre 0 y 2pi.
    if oveja.vivo == True:
        theta = rand.choice(np.linspace(0,2*np.pi,100))
        oveja.pos = oveja.pos + oveja.vel*np.array([np.cos(theta), np.sin(theta)])
    else:
        pass

def movimiento_zorro(zorro):
    #el movimeinto de la oveja consiste en moverse velocidad*vector director para el vector director necesito un angulo
    #theta entre 0 y 2pi.
    if zorro.vivo == True:
        theta = rand.choice(np.linspace(0,2*np.pi,100))
        zorro.pos = zorro.pos + zorro.vel*np.array([np.cos(theta), np.sin(theta)])

def muerte_oveja(oveja, t):
    if t>=oveja.tiempo_de_vida and oveja.vivo == True:
        oveja.vivo = False
        oveja.tiempo_muerta = t

def muerte_zorro(zorro, t):
    if t>=zorro.tiempo_de_vida and zorro.vivo == True:
        zorro.vivo = False
        zorro.tiempo_muerta = t



def movimiento_arbol(arbol):
    #el movimeinto de la oveja consiste en moverse velocidad*vector director para el vector director necesito un angulo
    #theta entre 0 y 2pi.
    pass
