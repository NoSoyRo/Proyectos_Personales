from choques import *

# L = [particula(1, np.array([-3,0]), np.array([1,0]), 1, 0), 
#      particula(1, np.array([0,0]), np.array([0,0]), 1, 1),
#      particula(1, np.array([3,0]), np.array([-1,0]), 1, 2)] 


L = [particula(1, np.array([0,2]), np.array([0,-1]), 1, 0), 
     particula(1, np.array([0,-2]), np.array([0,1]), 1, 1)]
#      particula(1, np.array([3,0]), np.array([-1,0]), 1, 2)] 

exp = experimento(L, 5, 5)
exp.realiza_el_experimento(500, 0.1)
