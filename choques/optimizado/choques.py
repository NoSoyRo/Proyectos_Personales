import numpy as np

class particula():
    def __init__(self, m, p, vn, va, r):
        self.m, self.p, self.vn, self.va, self.r = m,p,vn,va,r

class nodo():
    # el nodo guarda un objeto de tipo partícula
    def __init__(self, part, izquierda = None, derecha = None): 
        self.i,self.d,self.part = izquierda, derecha, part

def abs(x):
    if x<0:
        return(-x)
    else:
        return(x)

def sqrt(x):
    return(x**0.5)

def dist(p1, p2):
    dist = sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
    return(dist)

def vunit_12(p1, p2):
    vect = (p2-p1)/dist(p1, p2)
    return(vect)

def Arbol2D(listauwu, profundidad: int = 0): 
    if len(listauwu) == 0:
        return None
    eje = profundidad % 2
    #ordenamos la lista de objetos usando el eje definido por la profundidad.
    lista = listauwu
    lista.sort(key = lambda x: x.p[eje]) 
    media = len(lista) // 2
    return(nodo(part      = lista[media],
                izquierda = Arbol2D(lista[:media]  , profundidad+1),
                derecha   = Arbol2D(lista[media+1:], profundidad+1)))

### BPI == Búsqueda de partículas traslapadas

def Arbol2D_BPT(raiz, punto, Rc, L, p = 0, k = 2):
    if raiz is None:    
        return(L, F_punto_por_raiz)
    eje = p%2
    sb = None
    ob = None
    if punto.p[eje] < raiz.part.p[eje]:
        sb = raiz.i
        ob = raiz.d
    else:
        sb = raiz.d
        ob = raiz.i
    # Esta parte solo calcula si una particula entra o no al radio critico.
    if (dist(raiz.part.p,punto.p)<=(raiz.part.r + punto.r)) and ((raiz.part.p != punto.p).any()):
        #print(raiz.part.p,punto.p) #####
        L.append(raiz.part)
    # Recursion.
    L, F_punto_por_raiz = Arbol2D_BPT(sb, punto, Rc, L, 
                                      p+1, k=2, F_punto_por_raiz=F_punto_por_raiz)
    if Rc > abs(raiz.part.p[eje]-punto.p[eje]):
        L, F_punto_por_raiz = Arbol2D_BPT(ob, punto, Rc, L, p+1, k=2, F_punto_por_raiz=F_punto_por_raiz)
    return(L)