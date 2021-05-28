import numpy as np
from numpy import random as rand

#caract_ovejas = {
#    "velocidad"      : 1,
#    "tiempo_de_vida" : 20,
#    "pos_0"          : np.array([0,0])
#    "vivo"           : True
#}

class oveja():
    def __init__(self, caract_ovejas):
        self.vel            = caract_ovejas["velocidad"]
        self.tiempo_de_vida = caract_ovejas["tiempo_de_vida"]
        self.pos            = caract_ovejas["pos_0"]
        self.vivo           = caract_ovejas["vivo"]

class zorro():
    def __init__(self, caract_zorro):
        self.vel            = caract_zorro["velocidad"]
        self.tiempo_de_vida = caract_zorro["tiempo_de_vida"]
        self.pos            = caract_zorro["pos_0"]
        self.vivo           = caract_zorro["vivo"]

class arbol():
    def __init__(self, caract_arbol):
        self.vel            = caract_arbol["velocidad"]
        self.tiempo_de_vida = caract_arbol["tiempo_de_vida"]
        self.pos            = caract_arbol["pos_0"]


