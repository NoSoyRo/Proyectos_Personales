import objetos_n_cpos as objs
import numpy as np

dicc = {
    'n_parts': 3,
    'mmin': 50,
    'mmax': 100,
    'vxmin': -1,
    'vxmax': 1,
    'xmin': -20,
    'xmax': 20,
    'vymin': -3,
    'vymax': 1,
    'ymin': -20,
    'ymax': 20,
    'Rc': 20,
}

# L = [objs.particula(np.array((7, 2)),np.array((1, 0)),1), 
#      objs.particula(np.array((5, 4)),np.array((1, -1)),1), 
#      objs.particula(np.array((9, 6)),np.array((1, 0)),1), 
#      objs.particula(np.array((4, 7)),np.array((1, -1)),1), 
#      objs.particula(np.array((8, 1)),np.array((1, 0)),1), 
#      objs.particula(np.array((2, 3)),np.array((1, 1)),1), 
#      objs.particula(np.array((6, 1)),np.array((1, 1)),1), 
#      objs.particula(np.array((10, 1)),np.array((1, -1)),1)]
# L = [objs.particula(np.array((7, 2)),np.array((0, 0)),1), 
#      objs.particula(np.array((5, 4)),np.array((0, 0)),1), 
#      objs.particula(np.array((9, 6)),np.array((0, 0)),1), 
#      objs.particula(np.array((4, 7)),np.array((0, 0)),1), 
#      objs.particula(np.array((8, 1)),np.array((0, 0)),1), 
#      objs.particula(np.array((2, 3)),np.array((0, 0)),1), 
#      objs.particula(np.array((6, 1)),np.array((0, 0)),1), 
#      objs.particula(np.array((10, 1)),np.array((0, 0)),1)]
L = [objs.particula(np.array((7, 2)),np.array((-1.2, 0)),5,0), 
     objs.particula(np.array((5, 4)),np.array((1.2, 0)),5,1)]
exp01 = objs.Experimento(dicc)
exp01.lista_de_particulas(L)
exp01.realiza_el_experimento(60, 1000)
