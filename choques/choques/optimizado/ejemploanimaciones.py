import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import herramientas_de_analisis_de_resultados as h
from herramientas_de_analisis_de_resultados import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calcula_KyKmean(t: int,v: pd.DataFrame, mr: pd.DataFrame):
    if 'magv' not in v.columns.to_list():
        v["magv"] = np.sqrt(v['vx']**2 + v['vy']**2)
    a = v[v['t'] == t].merge(mr, how = 'left', on = 'idx')
    k_tot = 1/2*np.sum((a['magv']**2)*(a['m']))
    kmean = k_tot/a.shape[0]
    return(k_tot, kmean)

# Calcula la temperatura del sistema

def calcula_temp(K_mean: float, R = 8.314):
    return((2/3)*(1/R)*K_mean)

def mb(v, T, m, kb = 1.38E-23):
    t1 = 4*np.pi
    t2 = (m/(2*kb*np.pi*T))**(3/2)
    t3 = (v**2)*(np.exp(-(m*v**2)/(2*kb*T)))
    return(t1*t2*t3)

p,v,mr,dt = h.cambio_a_pandas(r"C:\Users\rodri\Documents\Proyectos_Personales\choques\choques\optimizado\dinamica.txt", 800)
v["magv"] = np.sqrt(v['vx']**2 + v['vy']**2)

k1,k2 = calcula_KyKmean(999, v, mr)

Temp = calcula_temp(k2)

velo = np.linspace(0,3,1000)
pv = []
for i in velo:
    pv.append(mb(i, Temp, 1))

fig     = plt.figure()
ax      = plt.axes(xlim = (0,5), ylim = (0,1.3))
scatter = ax.scatter(p[p['t'] == 0]['x'],p[p['t'] == 0]['y']) 

def anim(i):
    scatter.set_offsets(p[p['t']] == i)
    return(scatter)

simu = animation.FuncAnimation(fig, anim, frames=100)
plt.show()