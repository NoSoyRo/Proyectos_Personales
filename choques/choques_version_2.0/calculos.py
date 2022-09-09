import gas_choques as gsch
import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as lng
import time


start_time = time.time()

Listanps = [10,20,30,40,50,60,70,80,90,100]

figure, axis = plt.subplots(3, 1)


for i in Listanps:
    Particulas_i = gsch.gen_n_parts(i,10,10,10,10,1,0.2)
    Particulas_i.append(gsch.p(np.array([-10+0.2,10-0.2]),np.array([1,-1]),1,1))
    Pos,Vel,T = gsch.dinamica(Particulas_i,10,5,5)
    print("tardó", time.time()-start_time)

    X,Y = gsch.regresax_y_y(Pos,-1)
    VX,VY = gsch.regresax_y_y(Vel,-1)

    Mags = []

    for i,j in zip(VX,VY):
        Mags.append((i**2+j**2)**(1/2))

    axis[0].plot(X,Y)
    axis[1].plot(T,VX)
    axis[1].plot(T,VY)
    axis[2].plot(T,Mags)
#axis[0].set_title("(X,Y) DE LA PARTÍCULA.")
#axis[1].set_title("T VS VX Y T VS VY.")
#axis[2].set_title("T VS MAGNITUD DE V")
plt.show()