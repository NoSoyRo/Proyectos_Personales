import numpy as np
from numpy import random as rand

# Partícula importante.

class particula(): 
    # objeto para modelar las partículas del sistema 
    def __init__(self, p,v,m, identificador):
        self.p,self.v,self.m,self.idx = p,v,m,identificador
    def __str__(self):
        return('con posición en: 'f'{self.p}')

# Nodo para generar el arbol.

class nodo():
    # el nodo guarda un objeto de tipo partícula
    def __init__(self, part, izquierda = None, derecha = None): 
        self.i,self.d,self.part = izquierda, derecha, part

# Funcion importante para poder calcular los cm adecuados para cada 
# subarbol.

def abs(x):
    if x<0:
        return(-x)
    else:
        return(x)

def sqrt(x):
    return(x**0.5)

def dist(p1, p2):
    dist = sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
    #print(dist, p1, p2, p1[0]- p2[0], p1[1]- p2[1])
    return(dist)

def vunit_12(p1, p2):
    #print(p1,p2)
    vect = (p2-p1)/dist(p1, p2)
    return(vect)

def calccm(lista):
    cm, mt= np.array([0,0]), 0
    for i in lista:
        cm += i.m*i.p
        mt += i.m
    return([cm/mt, mt])

# Funcion que calcula la fuerza de la masa y del cm de las partículas que no entran papu.

def F_en1por2(obj1: particula, obj2: particula):
    G = 1 #6.6E-11
    cte = G*obj1.m*obj2.m
    Fuerza = cte * ((dist(obj1.p, obj2.p))**(-2)) * (vunit_12(obj1.p, obj2.p))
    return(Fuerza)

# Árbol que tiene una lista de objetos [particula1, particula2, ...]
# El arbol tiene nodos-hojas que tienen como dato guardado el objeto particula
# de modo que para poder acceder por ejemplo a la posicion de la primera particula
# a la izquierda del nodo raiz hay que hacer 
# arbol.i.part.p = posicion de dicha partícula.

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
                derecha   = Arbol2D(lista[media+1:], profundidad+1)))  ######### Re checar lo de los centros de masa.

# BPR == Búsqueda de Partículas en un Radio
# Ya tengo la búsqueda que es una funcion que me regresa
# una lista de elementos mas cercanos a punto, son PARTÍCULAS. 
# Tambien devuelve la fuerza que siente dicha partícula por todas las que se encuentran dentro de la B_RC(punto)

def Arbol2D_BPR(raiz, punto, Rc, L, p = 0, k = 2, F_punto_por_raiz = np.array([0,0])):
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
    if (dist(raiz.part.p,punto.p)<=Rc) and ((raiz.part.p != punto.p).any()):
        #print(raiz.part.p,punto.p) #####
        L.append(raiz.part)
        Fuerza = F_en1por2(punto, raiz.part)
        F_punto_por_raiz = F_punto_por_raiz + Fuerza
    # Recursion.
    L, F_punto_por_raiz = Arbol2D_BPR(sb, punto, Rc, L, 
                                      p+1, k=2, F_punto_por_raiz=F_punto_por_raiz)
    if Rc > abs(raiz.part.p[eje]-punto.p[eje]):
        L, F_punto_por_raiz = Arbol2D_BPR(ob, punto, Rc, L, p+1, k=2, F_punto_por_raiz=F_punto_por_raiz)
    return(L, F_punto_por_raiz)

# Función para obtener las partículas fuera del radio crítico.

def particulas_fuera_del_radio(LPDENTRO, LPTOTAL, punto):
    #print([i.p for i in LPDENTRO], [i.p for i in LPTOTAL])
    #print(LPDENTRO,LPTOTAL, LPDENTRO[0] == LPTOTAL[0])
    print()
    fuera_del_radio = list(set(LPTOTAL)-set(LPDENTRO+[punto]))
    #print(fuera_del_radio[])
    return(fuera_del_radio)

#Función para calcular el cm de las partículas fuera del radio crítico

def calcula_cm_de_particulas_fuera_del_radio(L: list):
    if len(L) == 0:
        return(np.array([0,0]),0)
    m_fuera        = 0
    rcm_fuera      = np.array([0,0])
    for i in L:
        m_fuera   = m_fuera + i.m
        rcm_fuera = rcm_fuera + i.m * i.p
    return(rcm_fuera/m_fuera, m_fuera)

# A continuación tenemos las funciones para atravesar completamente un arbol
# Servirá para encontrar para cada elemento los nodos que estan fuera del alcance 
# del radio crítico entonces ahora si hay que idear ese algoritmo con el fin de pensar
# como le haré para aproximar, porque debo tener en cuenta que cada sub arbol deberá
# tener el cm de todo lo que resta.

# funcion para escribir las posiciones en un archivo, las velocidades en un archivo

def redaccion_de_texto(L):
    pos = open('posiciones.txt','a')
    vel = open('velocidades.txt','a')
    for i in L:
        pos.write('('+str(tuple(i.p)[0])+';'+str(tuple(i.p)[1])+';'+str(i.idx)+')'+',')
        vel.write('('+str(tuple(i.v)[0])+';'+str(tuple(i.v)[1])+';'+str(i.idx)+')'+',')
    pos.write('\n')
    vel.write('\n')
    pos.close()
    vel.close()

###############################no necesarias
def preorden(a2d):
    #visita la raiz
    print(a2d.part)
    #recorre el arbol izquierdo
    try:
        preorden(a2d.i)
    except:
        None
    #recorre el arbol derecho
    try:
        preorden(a2d.d)
    except:
        None

def inorden(a2d):
    try:
        inorden(a2d.i)
    except:
        None
    print(a2d.part)
    try:
        inorden(a2d.d)
    except:
        None

def postorden(a2d):
    try:
        postorden(a2d.i)
    except:
        None
    try:
        postorden(a2d.d)
    except:
        None
    print(a2d.part)
###############################no necesarias
class Experimento():
    # come un diccionario que tiene:
    # mmin, mmax, n_parts, xmin, xmax, ymin, ymax, vxmin, vxmax, vymin, vymax
    def __init__(self, dicc):
        self.n_parts           = dicc['n_parts']
        self.mmin, self.mmax   = dicc['mmin'], dicc['mmax']
        self.vxmin, self.vxmax = dicc['vxmin'], dicc['vxmax']
        self.xmin, self.xmax   = dicc['xmin'], dicc['xmax']
        self.vymin, self.vymax = dicc['vymin'], dicc['vymax']
        self.ymin, self.ymax   = dicc['ymin'], dicc['ymax']
        self.Rc                = dicc['Rc']
    # Método para generar las partículas en el espacio de 2D.
    def genera_particulas_aleatorias(self):
        self.Lista_de_parts = []
        rango_de_pos_x = np.linspace(self.xmin,self.xmax,1000)
        rango_de_pos_y = np.linspace(self.ymin,self.ymax,1000)
        rango_de_vel_x = np.linspace(self.vxmin,self.vxmax,1000)
        rango_de_vel_y = np.linspace(self.vymin,self.vymax,1000)
        rango_de_masas = np.linspace(self.mmin,self.mmax,1000)
        # calculamos el centro de masa y la masa completa
        self.m_tot     = 0
        self.rcm_tot   = np.array([0,0])
        for i in range(self.n_parts):
            masa_i, x_i, y_i = rand.choice(rango_de_masas),rand.choice(rango_de_pos_x),rand.choice(rango_de_pos_y)
            vxi, vyi = rand.choice(rango_de_vel_x), rand.choice(rango_de_vel_y)
            self.Lista_de_parts.append(particula(p = np.array([x_i,y_i]),
                                                 v = np.array([vxi,vyi]),
                                                 m = masa_i,
                                                 identificador = i))
            self.m_tot = self.m_tot + masa_i
            self.rcm_tot = self.rcm_tot + masa_i*np.array([x_i,y_i])
        self.rcm_tot = self.rcm_tot/self.m_tot 
    def lista_de_particulas(self, lista):
        self.Lista_de_parts = lista
    # Método para realizar el experimento o la simulación computacuional.
    # ut =  unidades de tiempo
    def realiza_el_experimento(self, fps: int, ut: int, pasos_temporales = 's'):
        # ya que tenemos las partículas generadas, tenemos que calcular los fps
        # dicc = {'s': 1, 'm': 60, 'hr': 3600} #implementar mas escalas de tiempo.
        # n_frames = fps * ut * dicc[pasos_temporales]
        # self.dt = dicc[pasos_temporales]
        self.dt = 0.1
        n_frames = 500
        for i in range(n_frames):
            arbol = Arbol2D(self.Lista_de_parts)
            redaccion_de_texto(self.Lista_de_parts)
            for j in self.Lista_de_parts:
                Lista, force = Arbol2D_BPR(arbol, j, 2, [], p=0)
                L_fuera      = particulas_fuera_del_radio(Lista, self.Lista_de_parts, j)
                print('calculo la fuerza de la partícula', j, 'usando las partículas dentro: ', [i.p for i in Lista], 'y las partículas fuera: ', [i.p for i in L_fuera])
                je,jeje      = calcula_cm_de_particulas_fuera_del_radio(L_fuera)
                F_fuera      = F_en1por2(j, particula(je,np.array([0,0]),jeje,-1))
                F_tot        = force + F_fuera
                j.v          = j.v + (self.dt/j.m) * F_tot
                j.p          = j.p + (self.dt * j.v)
                print('la posicion de esta partícula es: ', j, '\n\n')
######################## TESTEO ########################
# ARBOLES

# L = [particula(np.array((7, 2)),np.array((7, 2)),1), 
#      particula(np.array((5, 4)),np.array((7, 2)),1), 
#      particula(np.array((9, 6)),np.array((7, 2)),1), 
#      particula(np.array((4, 7)),np.array((4, 7)),1), 
#      particula(np.array((8, 1)),np.array((3, 7)),1), 
#      particula(np.array((2, 3)),np.array((2, 7)),1), 
#      particula(np.array((6, 1)),np.array((1, 7)),1), 
#      particula(np.array((10, 1)),np.array((4, 7)),1)]

# arbol = Arbol2D(L)

# #list_aux = preorden(arbol)

# ### prueba de que sirve la busqueda Arbol2D_BPR.
# for i in L:
#     Lista, force = Arbol2D_BPR(arbol,i, 2, [], p=0)
#     L_fuera   = particulas_fuera_del_radio(Lista, L)
#     A,B       = calcula_cm_de_particulas_fuera_del_radio(L_fuera)
#     F_fuera   = F_en1por2(i, particula(A,np.array([0,0]),B))
#     F_tot     = force + F_fuera
#     i.p   = i.p + ((((1)**2/i.m)*F_tot))
### prueba para ver la eliminación de elementos 

#L_i = L[0:2]

#print(L_i[0] == L[1], L[0].p)

### prueba para ver las funciones de cm:

#print(calcula_cm_de_particulas_fuera_del_radio(L_i))

### prueba de la función redaccion_de_texto

# redaccion_de_texto(arbol)

### TODO MAS IMPORTANTE.
## Básicamente tengo dos problemas aun por resolver: 
# el encontrar los nodos mas cercanos a cada nodo. ya!
# y saber como implementar lo del centro de masa.  ya!


#### DEBUG: El problema del algoritmo seguro tiene que ver con los += que tenía, ver por qué los += no jalan y
####        seguro con eso sale el problema.