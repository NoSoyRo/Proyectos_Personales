import numpy as np
import vpython as vp
from numpy import random as rand
import matplotlib.pyplot as plt
cond_ini_def = {
                "tiempo_ini": 0,
                "dt": 0.01,
                "num_parts_izq": 10,
                "num_parts_der": 5,
                "long_rect_izq": 10,
                "long_rect_der": 5,
                "radio_izq": 1,
                "radio_der": 2,
                "lim_inf_vel_izq": -1,
                "lim_sup_vel_izq": 1,
                "lim_inf_vel_der": -1,
                "lim_sup_vel_der": 1,
                "altura": 2,
                "profundidad": 0
                }
class codiciones_iniciales():
    def __init__(self,dic):
        self.l_izq = dic["long_rect_izq"] 
        self.l_der = dic["long_rect_der"]
        self.t_0 = dic["tiempo_ini"]
        self.dt = dic["dt"]
        self.n_p_izq = dic["num_parts_izq"]
        self.n_p_der = dic["num_parts_der"]
        self.r_izq = dic["radio_izq"]
        self.r_der = dic["radio_der"]
        self.alturay = dic["altura"]
        self.profz = dic["profundidad"]

        self.plongizqx = np.linspace(-self.l_izq+2*self.r_izq, self.l_izq-2*self.r_izq, 100) #2 radios pa que pueda haber una partícula en el mero borde!
        self.plongderx = np.linspace(-self.l_der+2*self.r_der, self.l_der-2*self.r_der, 100)
        
        self.alturasizq = np.linspace(-self.alturay*0.5+2*self.r_izq, self.alturay*0.5-2*self.r_izq, 100)
        self.alturasder = np.linspace(-self.alturay*0.5+2*self.r_der, self.alturay*0.5-2*self.r_der, 100)
        
        self.profizq = np.linspace(-self.profz*0.5+2*self.r_izq, self.profz*0.5-2*self.r_izq, 100)
        self.profder = np.linspace(-self.profz*0.5+2*self.r_der, self.profz*0.5-2*self.r_der, 100)
        
        self.velspart_izq = np.linspace(dic["lim_inf_vel_izq"],dic["lim_sup_vel_izq"],100) 
        self.velspart_izq = np.linspace(dic["lim_inf_vel_der"],dic["lim_sup_vel_der"],100) 
        
        

    def particulas_pos_vel(self):
        self.pos_i_vecizq = [vp.vector(rand.choice(self.plongizq),
                         rand.choice(self.alturasizq),
                         rand.choice(self.profizq)) for i in range(self.n_p_izq)]
        self.vel_i_vectizq = [vp.vector(rand.choice(self.velspart_izq),
                         rand.choice(self.velspart_izq),
                         rand.choice(self.velspart_izq)) for i in range(self.n_p_izq)]
        self.pos_i_vectder = [vp.vector(rand.choice(self.plongder),
                         rand.choice(self.alturasder),
                         rand.choice(self.profder)) for i in range(self.n_p_der)]
        self.vel_i_vectder = [vp.vector(rand.choice(self.velspart_der),
                         rand.choice(self.velspart_izq),
                         rand.choice(self.velspart_izq)) for i in range(self.n_p_der)]
        
        #objetitos
        self.particulas_izq = [vp.sphere(pos = i, radius = self.r_izq, color = vp.vector(1,1,1)) for i in self.pos_i_vecizq]
        self.particulas_der = [vp.sphere(pos = i, radius = self.r_izq, color = vp.vector(1,1,0)) for i in self.pos_i_vecder]
        #vels
        for i,j in zip(self.pos_i_vecizq, self.vel_i_vectizq):
            i.vel = j
        for i,j in zip(self.pos_i_vecder, self.vel_i_vectder):
            i.vel = j
        #correccion traslapes
        ##izqx
        for i in self.pos_i_vecizq:
            for j in self.plongizqx:
                if j != i:
                    if vp.mag(j.pos-i.pos) < 2*r_p:
                        lambda_1 = (2*self.r_izq-(vp.mag(i.pos-j.pos)))/(vp.mag(i.vel))
                        i.pos = i.pos + lambda_1*i.vel
        ##derx
        for i in self.pos_i_vectder:
            for j in self.plongderx:
                if j != i:
                    if vp.mag(j.pos-i.pos) < 2*r_p:
                        lambda_2 = (2*self.r_izq-(vp.mag(i.pos-j.pos)))/(vp.mag(i.vel))
                        i.pos = i.pos + lambda_1*i.vel
        #juntamos todo
        self.parts_tot = self.particulas_izq + self.particulas_der
        return(self.parts_tot)

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

condiciones = codiciones_iniciales(cond_ini_def)
particulas = condiciones.particulas_pos_vel()

while t<10:
    vp.rate(250)
    for particula in particulas:
        particula.pos = particula.pos + dt * particula.vel
        for i in particulas:
            if i != particula:
                colision_part_2(particula, i)
        rebote_particula_caja(particula)
    camino.append(pos = particulas[0].pos)
    #mediciones
    K = mediciones(particulas)
    energia_kin_en_cada_tiempo.append(K)
    tiempo.append(t)
    t=t+dt
