import numpy as np
import vpython as vp
from numpy import random as rand

cond_ini = {
            "num_parts_dentro" : 20,
            "num_parts_anillo" : 30,
            "radio_anillo" : 5,
            "carga_libre" : 1.5,
            "carga_anillo" : 2,
            "v_max" : 1,
            "v_min" : -1,
            "masa_libre" : 1,
            "masa_anillo" : 1,
}

dt = 0.01
t_max = 10
t = 0
ka = 1

Particulas_libres = []
Particulas_anillo = []
#posiciones de discretizacion del anillo
for i in range(cond_ini["num_parts_anillo"]): 
    p_0 = (cond_ini["radio_anillo"]) * vp.vector(np.cos((2*np.pi*i)/(cond_ini["num_parts_anillo"])),np.sin((2*np.pi*i)/(cond_ini["num_parts_anillo"])),0)
    part_i = vp.sphere(pos = p_0, radius = 0.3, color = vp.vector(1,1,1))
    part_i.carga = cond_ini["carga_anillo"]
    part_i.momento = vp.vector(0,0,0)
    Particulas_anillo.append(part_i)
#partículas dentro
for i in range(cond_ini["num_parts_dentro"]):
    r_part = np.linspace(0, cond_ini["radio_anillo"]*0.75, 100)
    theta_part = np.linspace(0, 2*np.pi, 100)
    r_i = rand.choice(r_part)
    theta_i = rand.choice(theta_part)
    p_0 = r_i*(vp.vector(np.cos(theta_i), np.sin(theta_i), 0))
    part_i = vp.sphere(pos = p_0, radius = 0.3, color = vp.vector(1,0,1))
    #pa vels
    vel_part = np.linspace(cond_ini["v_min"],cond_ini["v_max"],100)
    vel_i = vp.vector(rand.choice(vel_part),rand.choice(vel_part),0)
    part_i.vel = vel_i
    part_i.carga = cond_ini["carga_libre"]
    part_i.momento = cond_ini["masa_libre"]*part_i.vel
    part_i.masa = cond_ini["masa_libre"]
    #guardamso en lista:
    Particulas_libres.append(part_i)
#dinámica
while t < t_max:
    vp.rate(100)
    for i in Particulas_libres:
        F_tot_i = vp.vector(0,0,0)
        for j in Particulas_libres:
            if i != j:
                mag = (ka*i.carga*j.carga)/(vp.mag(i.pos-j.pos)**2)
                r_un_j_i = vp.norm(i.pos-j.pos)
                F_tot_i += mag*r_un_j_i
        for k in Particulas_anillo:
            mag = (ka*i.carga*k.carga)/(vp.mag(i.pos-k.pos)**2)
            r_un_k_i = vp.norm(i.pos-k.pos)
            F_tot_i += mag*r_un_k_i
        #dinamica:
        i.momento = i.momento + dt*F_tot_i
        i.pos = i.pos + (dt/i.masa)*i.momento
    t+=dt
