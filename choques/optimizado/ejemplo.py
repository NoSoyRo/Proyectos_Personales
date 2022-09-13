from choques import *

L = [particula(1, np.array([-0.5,0]), np.array([1,0]), np.array([1,0]), 0.5, 0), 
     particula(1, np.array([0.5,0]), np.array([-1,0]), np.array([-1,0]), 0.5, 1)] 

exp = experimento(L, 2, 2)
exp.realiza_el_experimento(5, 0.1)
