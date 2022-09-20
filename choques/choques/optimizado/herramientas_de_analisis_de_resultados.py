"""
Archivo que se utiliza para convertir dinamica e info_util en dataframes para estudiar de manera estadística los resultados de n experimentos, dentro de la generación
de los experimentos es importante notar que tengo que crear yo las partículas que me ayudarán a resolver el problema.

La idea ahora es que este módulo solo tome herramientas para convertir lo que tenemos en dataframes útiles y fáciles de manejar.
"""

import pandas as pd
import numpy as np
import re


def cambio_a_pandas(url_documento, n_parts):
    datos           = open(url_documento)
    list_pos        = []
    list_vel        = []
    list_masa_radio = []
    for line in datos:
        list_i = line.split(',')
        t  = int(list_i[-1])
        dt = float(list_i[-2])
        for i in range(n_parts):
            caracts_i = list_i[i][1:-1].split(';')
            x   = float(caracts_i[0])
            y   = float(caracts_i[1])
            vx  = float(caracts_i[2])
            vy  = float(caracts_i[3])
            idx = int(caracts_i[6])
            if t == 0:    
                m   = float(caracts_i[4])
                r   = float(caracts_i[5])
                list_masa_radio.append([idx, m, r])
            list_pos.append([idx, x, y, t])
            list_vel.append([idx, vx, vy, t])
    posi     = pd.DataFrame(list_pos,columns=['idx', 'x', 'y', 't'])
    velo     = pd.DataFrame(list_vel,columns=['idx', 'vx', 'vy', 't'])
    masyrad  = pd.DataFrame(list_masa_radio,columns=['idx', 'm', 'r'])
    return(posi, velo, masyrad, dt)
    

### Ejemplo de como funciona.
p,v,mr,dt = cambio_a_pandas(r"C:\Users\rodri\Documents\Proyectos_Personales\choques\optimizado\dinamica.txt", 2)

print(p)