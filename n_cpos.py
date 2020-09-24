import numpy as np
import vpython as vp

rango_masas = 1/10000
longitud = 100
n = 100

t=0
dt=1

masas = []
r_ini = []
v_ini = []
m_ini = []

G = 100

#posiciones iniciales:
#velocidades iniciales:
#masas:

def cond_ini(n, rango_masas, longitud, r_ini, v_ini, m_ini):
    for i in range(n):
        masa_i = np.random.rand()*rango_masas
        r_ini_i = vp.vector(np.random.choice(np.linspace(-0.1,0.1,10))*longitud,
                            np.random.choice(np.linspace(-0.1,0.1,10))*longitud,
                            np.random.choice(np.linspace(-0.1,0.1,10))*longitud)
        v_ini_i = vp.vector(np.random.choice(np.linspace(-0.1,0.1,10))*longitud,
                            np.random.choice(np.linspace(-0.1,0.1,10))*longitud,
                            np.random.choice(np.linspace(-0.1,0.1,10))*longitud)
        #v_ini_i = vp.vector(0,0,0)
        m_ini_i = masa_i*v_ini_i

        masas.append(masa_i)
        r_ini.append(r_ini_i)
        v_ini.append(v_ini_i)
        m_ini.append(m_ini_i)

def mag_fza(pos_1, pos_2, m_1, m_2):
    r = vp.mag(pos_2-pos_1)
    m_f = (G*m_1*m_2)/(r**2)
    return(m_f)

def fza_vect(mag_fza, pos_1, pos_2):
    vect = mag_fza*vp.hat(pos_2-pos_1)
    return(vect)

cond_ini(n, rango_masas, longitud, r_ini, v_ini, m_ini)

r=[r_ini]
v=[v_ini]
m=[m_ini]

#objetos:
planetas = [vp.sphere(pos = i, radius = 0.5) for i in r[0]]
orbitas = []

for i,j in zip(planetas, masas):
    i.masa = j #<--- agregamos masa al objeto 

#for i in planetas:                                 #
    #trail_i = vp.curve(color = vp.vector(1,0,0))   # ->  esto habilitarlo si quiero todos
    #orbitas.append(trail_i)                        #

trail_i = vp.curve(color = vp.vector(1,0,0)) #
orbitas.append(trail_i)                      # -> pa solo 1.

#fin objetos

########################################################hacer esto para alterar una masa a placer:

masas[0]=2
planetas[0].radius = 1
r[0][0] = vp.vector(-11,11,0)
v[0][0] = vp.vector(2,2,0)
m[0][0] = vp.vector(0,0,0)
#caso para momento iguala cero:

suma = vp.vector(0,0,0)

for i in m[0]:
    suma = suma+i

m[0][-1] = -suma

########################################################fin hacer esto para alterar una masa a placer
vp.scene.autoscale = False
while t<900:
    vp.rate(100)
    r_t = []
    m_t = []
    f_t = []
    for i,k,l in zip(r[-1], m[-1], planetas): # si quiero sin todas las orbitas entonces, quito x y orbitas o las agrego en caso contrario
        suma_f_i = vp.vector(0,0,0)
        for j in r[-1]:
            if i != j:
                fza_i_por_j = fza_vect(mag_fza(i, j, masas[r[-1].index(i)], masas[r[-1].index(j)]), i, j)
                suma_f_i = suma_f_i + fza_i_por_j
        ###momentos
        momento_i = k + dt * suma_f_i
        posiciones_i = i + (dt)*momento_i
        ###listas
        l.pos = posiciones_i
        #x.append(pos = l.pos) <- habilita si quieres todos los ptos planetas con seguimitento
        m_t.append(momento_i)
        r_t.append(posiciones_i)
    orbitas[0].append(pos = r[-1][0]) #<- habilita para solo 1 planeta con orbita 
    m.append(m_t)
    r.append(r_t)
    t=t+dt


print('Terminó el ciclo')

