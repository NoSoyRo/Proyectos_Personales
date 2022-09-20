from gas_choques import *

nparts_max = 101
ni = 1
tiempos = []
nparts = []
for i in range(1,nparts_max,5):
    start_time = time.time()
    Particulas_i = gen_n_parts(i,5,5,1,1,1,0.1)
    Pos,Vel,T = dinamica(Particulas_i,20,5,5)
    delta_t = time.time()-start_time
    tiempos.append(delta_t)
    nparts.append(i)

timeposlog = [np.log(i) for i in tiempos]
npartslog = [np.log(i) for i in nparts]

plt.scatter(nparts,tiempos)
plt.title("101 particulas de 5 en 5")
plt.show()
plt.scatter(npartslog,timeposlog)
plt.show()