from funciones_utiles import *
from zba import *

t = 0
dt = 0.01

caract_ovejas = {
    "velocidad"      : 0.1,
    "tiempo_de_vida" : 20,
    "pos_0"          : np.array([0,0]),
    "vivo"           : True
}

oveja_1 = oveja(caract_ovejas)

pos_x  = []
pos_y  = []
tiempo = []

while t<30:
    #guardamos posiciones y tiempo
    pos_x.append(oveja_1.pos[0])
    pos_y.append(oveja_1.pos[1])
    tiempo.append(t)
    #decido si muere o vive
    muerte_oveja(oveja_1,t)
    #actualizamos el movimeinto de la oveja
    movimiento_oveja(oveja_1)
    #
    t=t+dt

if oveja_1.vivo == False:
    print("oveja morida al timepo: ", oveja_1.tiempo_muerta)

plt.plot(pos_x,pos_y)
plt.show()
plt.plot(tiempo,pos_x)
plt.plot(tiempo,pos_y)
plt.show()