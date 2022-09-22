"""
Archivo que se utiliza para convertir dinamica e info_util en dataframes para estudiar de manera estadística los resultados de n experimentos, dentro de la generación
de los experimentos es importante notar que tengo que crear yo las partículas que me ayudarán a resolver el problema.

La idea ahora es que este módulo solo tome herramientas para convertir lo que tenemos en dataframes útiles y fáciles de manejar.
"""

import pandas as pd
import numpy as np
import re

# ETL de datos a dataframes de pandas.

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

# Cálculo de tiempo medio libre y distancia media libre.
    
def calcula_tmed_distmed(p: pd.DataFrame, v: pd.DataFrame, dt: float): #dt dato en info_util.txt
    v_dos            = v.drop_duplicates(['idx', 'vx', 'vy'],ignore_index=True)
    v_tres           = v_dos.sort_values(['idx', 't'], ignore_index=True)
    v_tres           = v_tres.merge(p, how = 'inner', on = ['idx', 't'])
    v_tres[v_tres['idx'].isin([1])].diff(periods = 1, axis = 0).dropna()
    v_cuatro         = v_tres.groupby(['idx']).diff(periods = 1, axis = 0).dropna()
    v_cuatro['dist'] = np.sqrt(v_cuatro['x']**2+v_cuatro['y']**2)
    tiempo_med       = v_cuatro['t'].mean()
    dist_med         = v_cuatro['dist'].mean()
    return(tiempo_med*dt, dist_med) # Nota que se multiplica tiempo por dt porque el tiempo med 
                                    # que se calcula es cuantos pasos da el algoritmo antes de chocar, 
                                    # por ende dado un dt dichos pasos por el dt es el tiempo que tardan 
                                    # en colisionar en promedio las partículas.

# Histogramas de magnitudes de la velocidad.

def crea_histograma_de_magdevelocidades(v: pd.DataFrame, t: int):
    if 'magv' not in v.columns.to_list():
        v["magv"] = np.sqrt(v['vx']**2 + v['vy']**2)
    v[v['t'] == t].hist('magv', bins = 50)

# Calcula la energia cinética promedio.

def calcula_KyKmean(t: int,v: pd.DataFrame, mr: pd.DataFrame):
    if 'magv' not in v.columns.to_list():
        v["magv"] = np.sqrt(v['vx']**2 + v['vy']**2)
    a = v[v['t'] == t].merge(mr, how = 'left', on = 'idx')
    k_tot = 1/2*np.sum((a['magv']**2)*(a['m']))
    kmean = k_tot/a.shape[0]
    return(k_tot, kmean)

# Calcula la temperatura del sistema

def calcula_temp(K_mean: float, R = 8.314):
    return((2/3)*(1/R)*K_mean)

def mb(v, T, m, kb = 1.38E-23):
    t1 = 4*np.pi
    t2 = (m/(2*kb*np.pi*T))**(3/2)
    t3 = (v**2)*(np.exp(-(m*v**2)/(2*kb*T)))
    return(t1*t2*t3)