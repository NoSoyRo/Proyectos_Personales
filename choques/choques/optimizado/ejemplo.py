import choques as ch
import numpy as np

# L = [particula(1, np.array([-3,0]), np.array([1,0]), 1, 0), 
#      particula(1, np.array([0,0]), np.array([0,0]), 1, 1),
#      particula(1, np.array([3,0]), np.array([-1,0]), 1, 2)] 

#Creamos las partículas que servirán para realizar el experimento
# masas positivas weon tonto
numpart     = 1000
lx          = 52
ly          = 7
idx         = 0
L           = []
masas       = np.linspace(0,1,100)         ### ULTRA PENDEJO LAS MASAS NO PUEDEN SER NEGATIVAS >:V
velocidades = np.linspace(-1,1,100)
for i in range(-50,50,10):
     for j in range(-5,5,1):
          masa_ij       = np.random.choice(masas)
          velocidad_ijx = np.random.choice(velocidades)
          velocidad_ijy = np.random.choice(velocidades)
          pos_ij = np.array([i,j])
          vel_ij = np.array([velocidad_ijx,velocidad_ijy])
          L.append(ch.particula(masa_ij, pos_ij, vel_ij, 0.3, idx))
          idx+=1

# L = [ch.particula(1, np.array([1,1]), np.array([-1,-0.5]), 0.5, 0),
# ch.particula(1, np.array([0,0]), np.array([-0.5,-0.1]), 0.5, 1)]

exp = ch.experimento(L, 52, 7)
exp.realiza_el_experimento(300, 0.1)
