import numpy as np
import vpython as vp
from numpy import random as rand

eps = 0.03   #<- valores recomendados para estabilidad
sigm = 0.005 #<- valores recomendados para estabilidad
n = int(input('Cantidad de moléculas: \n'))
longi = int(input('Longitud: \n'))
t = 0
dt = 0.01

def mag_fza(pos_1, pos_2):
    r = vp.mag(pos_2-pos_1)
    prod = 4*eps*(12*(sigm**(12)/(r**(13)))-6*((sigm**6)/(r**7)))
    return(prod)

def fza_vect(mag_fza, pos_1, pos_2):
    vect = mag_fza*vp.hat(pos_2-pos_1)
    return(vect)

def lim_mundo_caja(vector):
    if longi-vector.x < 0:
        vector.x = vector.x - longi
    if longi-vector.y < 0:
        vector.y = vector.y - longi
    if longi-vector.z < 0:
        vector.z = vector.z - longi
    if longi-vector.x > longi:
        vector.x = vector.x + longi
    if longi-vector.y > longi:
        vector.y = vector.y + longi
    if longi-vector.z > longi:
        vector.z = vector.z + longi
    
    
    return(vector)
    
    

posi_x_rand = [rand.rand()*longi for i in range(n)]
posi_y_rand = [rand.rand()*longi for i in range(n)]
posi_z_rand = [rand.rand()*longi for i in range(n)]

particion_menos_uno_mas_uno = np.linspace(-1,1,100)

veli_x_rand = [rand.choice(particion_menos_uno_mas_uno) for i in range(n)]
veli_y_rand = [rand.choice(particion_menos_uno_mas_uno) for i in range(n)]
veli_z_rand = [rand.choice(particion_menos_uno_mas_uno) for i in range(n)]

#veli_x_rand = [0 for i in range(n)]
#veli_y_rand = [0 for i in range(n)]
#veli_z_rand = [0 for i in range(n)]



pos_inicial = [vp.vector(i,j,k) for i,j,k in zip(posi_x_rand, posi_y_rand, posi_z_rand)]
vel_inicial = [vp.vector(i,j,k) for i,j,k in zip(veli_x_rand, veli_y_rand, veli_z_rand)]
momentos_iniciales = [i for i in vel_inicial]

lista_con_listas_posiciones_y_velocidades_iniciales = [[i,j] for i,j in zip(pos_inicial, vel_inicial)]

objetos_esferas = []

fzas = []
momentos = [momentos_iniciales]
posiciones = [pos_inicial]

while t<10:
    posiciones_t = []
    momentos_t = []
    fzas_t = []
    for i,k in zip(posiciones[-1], momentos[-1]):
        suma_f_i = vp.vector(0,0,0)
        for j in posiciones[-1]:
            if i != j:
                fza_i_por_j = fza_vect(mag_fza(i, j), i, j)
                suma_f_i = suma_f_i + fza_i_por_j
        ###momentos
        momento_i = k + dt * suma_f_i
        posiciones_i = i + (dt)*momento_i
        ###encierro en caja
        posiciones_i_c = lim_mundo_caja(posiciones_i)
        ###listas
        fzas_t.append(suma_f_i)
        momentos_t.append(momento_i)
        posiciones_t.append(posiciones_i_c)
    fzas.append(fzas_t)
    momentos.append(momentos_t)
    posiciones.append(posiciones_t)
    t=t+dt

###animación:

particulas = []

vp.scene.autoscale = False

for i in posiciones[0]:
    esfera_i = vp.sphere(pos = i, radius = 0.1)
    particulas.append(esfera_i)

for i in posiciones:
    for j,k in zip(particulas, i):
        vp.rate(250)
        j.pos = k

#este código puede ser mejorado; tomando en cuenta el cambio de posición, es decir:
#si el dr es muy gde, normalizarlo al tamaño de la caja o mundo
#la segunda forma que propongo es quitando el cambio y haciendo rebotes.
    
