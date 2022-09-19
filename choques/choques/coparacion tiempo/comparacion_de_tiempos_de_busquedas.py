from cmath import inf
from math import dist
import numpy as np
import time
import matplotlib.pyplot as plt

def abs(x):
    if x<0:
        return(-x)
    else:
        return(x)

def sqrt(x):
    return(x**0.5)

def dist_pot(p1, p2):
    if (p1 == p2).all():
        return(0)
    dist = (p1[0]-p2[0])**2+(p1[1]-p2[1])**2
    return(dist)

def dist(p1, p2):
    if p1 is None:
        return(float(inf))
    if p2 is None:
        return(float(inf))
    if (p1 == p2).all():
        return(0)
    dist = sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
    return(dist)

class nodo():
    # el nodo guarda un objeto de tipo partícula
    def __init__(self, part, izquierda = None, derecha = None): 
        self.i,self.d,self.p = izquierda, derecha, part

def Arbol2D(listauwu, profundidad: int = 0): 
    if len(listauwu) == 0:
        return None
    eje = profundidad % 2
    #ordenamos la lista de objetos usando el eje definido por la profundidad.
    lista = listauwu
    lista.sort(key = lambda x: x[eje]) 
    media = len(lista) // 2
    return(nodo(part      = lista[media], # lo que pertenece al nodo es un arreglo.
                izquierda = Arbol2D(lista[:media]  , profundidad+1),
                derecha   = Arbol2D(lista[media+1:], profundidad+1)))

def mascercano(pivot, p1, p2):
    if p1 is None:
        return p2

    if p2 is None:
        return p1

    d1 = dist_pot(pivot, p1)
    d2 = dist_pot(pivot, p2)

    if d1 < d2:
        return p1
    else:
        return p2

def Arbol2D_BPT(raiz: nodo, punto: np.array, mejor = None, p = 0, k = 2):
    if raiz is None:    
        return(None)
    eje = p%2
    sb = None
    ob = None
    if punto[eje] < raiz.p[eje]:
        sb = raiz.i
        ob = raiz.d
    else:
        sb = raiz.d
        ob = raiz.i

    mejor = mascercano(punto, Arbol2D_BPT(sb,punto,p + 1),raiz.p)
    
    if dist_pot(punto, mejor) > (punto[eje] - raiz.p[eje]) ** 2:
        mejor = mascercano(punto,Arbol2D_BPT(ob,punto,p + 1),mejor)

    return(mejor)

def busqueda_con_arbol(arbol, punto):
    mejor = Arbol2D_BPT(arbol, punto)
    return(mejor)

def busqueda_fuerza_bruta(lista, punto):
    mejor = None

    for i in lista:
        if dist(i, punto)<dist(mejor,punto):
            mejor = i
    return(mejor)

num_exps = 5
lista_de_lista_de_tiempos_de_arbol = []
lista_de_lista_de_tiempos_de_fzabr = []
for k in range(num_exps):
    tiempos_de_arbol_expk = []
    tiempos_de_fuerza_bruta_expk = []
    n_parts          = []
    for i in range(1, 10000, 500):#300001
        print(f"voy en el tiempo {i} \n")
        arr = np.random.rand(i, 2)
        Lista = [arr[j,:] for j in range(arr.shape[0])]
        arbol = Arbol2D(Lista)
        inicio = time.time()
        busqueda_con_arbol(arbol, np.array([0.1,0.1]))
        fin = time.time()
        tiempos_de_arbol_expk.append(fin-inicio)
        inicio = time.time()
        busqueda_fuerza_bruta(Lista, np.array([0.1,0.1]))
        fin = time.time()
        tiempos_de_fuerza_bruta_expk.append(fin-inicio)
        n_parts.append(i)
    lista_de_lista_de_tiempos_de_arbol.append(tiempos_de_arbol_expk)
    lista_de_lista_de_tiempos_de_fzabr.append(tiempos_de_fuerza_bruta_expk)


ind1 = 0
ind2 = 0
for i,j in zip(lista_de_lista_de_tiempos_de_arbol, lista_de_lista_de_tiempos_de_fzabr):
    plt.plot(n_parts, i,linestyle = 'dotted', marker = '.', markersize = 8,label = f'Exp. {ind1}; arbol')#, color = 'darkorange')
    plt.plot(n_parts, j,linestyle = 'dotted', marker = '.', markersize = 8,label = f'Exp. {ind2}; F. B.')#, color = 'darkcyan')
    plt.grid()
    plt.title('Tiempo que tardó vs cantidad de elementos \n sobre los que se hace la búsqueda.')
    ind1+=1
    ind2+=1
plt.legend()
plt.xlabel("Cantidad de elementos dentro de los cuales \n se hace la búsqueda.")
plt.ylabel("Tiempo que tarda en hacer la búsqueda.")
plt.show()


