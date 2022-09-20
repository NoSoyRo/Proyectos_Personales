import gas_choques as gsch
import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as lng
import time
import csv

start_time = time.time()
Particulas_i = gsch.gen_n_parts(1000,10,10,10,10,1,0.1)
Pos,Vel,T = gsch.dinamica(Particulas_i,20,5,5)

mags_vels = []
for i in range(len(T)):
    mags_vels_ti = []
    for j in Vel:
        mags_vels_ti.append(lng.norm(j[i]))
        #mags_vels_ti.append(j[i][1])
    mags_vels.append(mags_vels_ti)

f = open('datos_pos','w')
f1 = open('datos_vel','w')
writer = csv.writer(f)
writer1 = csv.writer(f1)
for i in range(len(T)):
    pos_ti = []
    vel_ti = []
    for j,k in zip(Pos,Vel):
        pos_ti.append(j[i])
        vel_ti.append(k[i])
    writer.writerow(pos_ti)
    writer1.writerow(vel_ti)
f.close()
plt.hist(mags_vels[-1], bins = 25)
plt.show()
print("tardó", time.time()-start_time)