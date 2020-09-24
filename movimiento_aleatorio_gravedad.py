import numpy as np
import vpython as vp
from numpy import random as rand
import matplotlib.pyplot as plt

campo_grav = vp.vector(0,-9.8,0) #<- se puede cambiar gravedad

n_p = int(input('Cuantas partículas? \n'))
r_p = float(input('Radio partículas \n'))
long_rect = float(input('Longitud del rectángulo \n'))
t = 0
dt = 0.01

particion_menos_uno_mas_uno = np.linspace(-10,10,100)


#longitud = np.linspace(-long_rect+r_p, long_rect-r_p, 100)

longitud = np.linspace(-10, 10, 100)

pos_i_vect = [vp.vector(rand.choice(longitud),
                         rand.choice(longitud),
                         rand.choice(longitud)) for i in range(n_p)]



vel_i_vect = [vp.vector(rand.choice(particion_menos_uno_mas_uno),
                         rand.choice(particion_menos_uno_mas_uno),
                         rand.choice(particion_menos_uno_mas_uno)) for i in range(n_p)]

particulas = [vp.sphere(pos = i, radius = r_p, color = vp.vector(1,1,1)) for i in pos_i_vect]

for i,j in zip(particulas, vel_i_vect):
    i.vel = j

for i in particulas: #<- cambiar pal caso de generalizacion de diferentes radios y diferentes masas
    i.mom = 1*i.vel

camino = vp.curve(color = vp.vector(1,0,0))

#listas pa mediciones:

energia_kin_en_cada_tiempo = []
energia_pot_en_cada_tiempo = []
energia_total = []
tiempo = []

#movimiento

#dinamica

def evita_traslapes(pos_i):
    for i in pos_i:
        for j in pos_i:
            if j != i:
                if vp.mag(j.pos-i.pos) < 2*r_p:
                    lambda_1 = (2*r_p-(vp.mag(i.pos-j.pos)))/(vp.mag(i.vel))
                    i.pos = i.pos + lambda_1*i.vel

def rebote_particula_caja(obj_1):
    if obj_1.pos.x+r_p > long_rect: 
        extra = (obj_1.pos.x+r_p) - long_rect
        obj_1.pos.x = obj_1.pos.x - (extra)
        obj_1.vel.x = -obj_1.vel.x
    elif obj_1.pos.x-r_p < -long_rect: 
        extra = (obj_1.pos.x-r_p)+long_rect
        obj_1.pos.x = obj_1.pos.x + np.abs(extra)
        obj_1.vel.x = -obj_1.vel.x

    if obj_1.pos.y+r_p > long_rect: 
        extra = (obj_1.pos.y+r_p) - long_rect
        obj_1.pos.y = obj_1.pos.y - (extra)
        obj_1.vel.y = -obj_1.vel.y
    elif obj_1.pos.y-r_p < -long_rect: 
        extra = (obj_1.pos.y-r_p)+long_rect
        obj_1.pos.y = obj_1.pos.y + np.abs(extra)
        obj_1.vel.y = -obj_1.vel.y

    if obj_1.pos.z+r_p > long_rect: 
        extra = (obj_1.pos.z+r_p) - long_rect
        obj_1.pos.z = obj_1.pos.z - (extra)
        obj_1.vel.z = -obj_1.vel.z
    elif obj_1.pos.z-r_p < -long_rect: 
        extra = (obj_1.pos.z-r_p)+long_rect
        obj_1.pos.z = obj_1.pos.z + np.abs(extra)
        obj_1.vel.z = -obj_1.vel.z

def colision_part_2(obj_1, obj_2):
    if vp.mag(obj_1.pos-obj_2.pos) < 2*r_p:
        delta_v_1 = obj_1.vel-obj_2.vel
        delta_p_1 = obj_1.pos-obj_2.pos
        delta_v_2 = obj_2.vel-obj_1.vel
        delta_p_2 = obj_2.pos-obj_1.pos

        coef_1 = (vp.dot(delta_v_1, delta_p_1))/(vp.dot(delta_p_1, delta_p_1))
        coef_2 = (vp.dot(delta_v_2, delta_p_2))/(vp.dot(delta_p_2, delta_p_2))
        
        obj_1.vel = obj_1.vel - coef_1*(obj_1.pos - obj_2.pos)
        obj_2.vel = obj_2.vel - coef_2*(obj_2.pos - obj_1.pos)

        lambda_1 = (2*r_p-(vp.mag(obj_1.pos-obj_2.pos)))/(vp.mag(obj_1.vel))
        obj_1.pos = obj_1.pos + lambda_1*obj_1.vel
#dinamica
#mediciones:

def mediciones(lista_de_particulas):
    suma_energias_cin = 0
    suma_energias_pot = 0
    for i in lista_de_particulas:
        suma_energias_cin = suma_energias_cin + (1/2)*(vp.mag(i.vel)**2) #<-- agregar masa en general recuerda que la masa es de 1 y los radios todos son iguales, podriamos generalizar en un futuro
        suma_energias_pot = suma_energias_pot + vp.mag(campo_grav)*np.absolute(i.pos.y+long_rect) #<- aqui iría tambien en mgh
    return((suma_energias_cin, suma_energias_pot))

#chequeo y cambio de cosas, pa checar que el codigo funcionase
particulas[0].color = vp.vector(1,0.6,0)
particulas[0].pos = vp.vector(0,1,0)
particulas[0].vel = vp.vector(0,0,0)
particulas[0].mom = vp.vector(0,0,0)
#particulas[1].vel = vp.vector(-1,0,0)
#particulas[1].pos = vp.vector(1.5,0,0)


while t<20:
    vp.rate(250)
    for particula in particulas:
        #calculo de fuerza:
        F_particula_peso = campo_grav
        #cambiamos el momento:
        particula.mom = particula.mom + dt*F_particula_peso
        #cambiamos la posición: <- cambiar cunaod haya masa a (dt/masa)*momento
        particula.pos = particula.pos + (dt)*particula.mom
        #debo actualizar la velocidad: <- cambiar cunaod haya masa a (1/masa)*momento
        particula.vel = particula.mom
        particula.pos = particula.pos + dt * particula.vel
        for i in particulas:
            if i != particula:
                  colision_part_2(particula, i)
        rebote_particula_caja(particula)
    camino.append(pos = particulas[0].pos)
    #mediciones
    K = mediciones(particulas)[0]
    U = mediciones(particulas)[1]
    T = K+U
    energia_kin_en_cada_tiempo.append(K)
    energia_pot_en_cada_tiempo.append(U)
    energia_total.append(T)  
    tiempo.append(t)
    t=t+dt

print('terminó la simulación \n')

plt.scatter(tiempo, energia_kin_en_cada_tiempo, label = 'energía cinética en el tiempo')
plt.scatter(tiempo, energia_pot_en_cada_tiempo, label = 'energía potencial en el tiempo')
plt.scatter(tiempo, energia_total, label = 'energía total en el tiempo')
plt.legend(loc = 'upper left')
plt.show()

