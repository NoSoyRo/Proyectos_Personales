import numpy as np

class particula():
    def __init__(self, m, p, v, r, identificador):
        self.m, self.p, self.v, self.r, self.idx = m,p,v,r,identificador
    def __str__(self):
        return(f'{self.p}')

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
    if (p1 == p2).all():
        return(0)
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

#Funcionq ue solo altera la velocidad nuev de la spartículas usando las velocidades antiguas de las partículas.

def dtt(obj1, obj2):
    dr   = obj2.p-obj1.p
    dv   = obj2.v-obj1.v
    drdr = dr[0]**2 + dr[1]**2
    dvdv = dv[0]**2 + dv[1]**2
    dvdr = ((dv[0])*(dr[0])) + ((dv[1])*(dr[1]))
    d    = (dvdr)**2 - (dvdv)*(drdr-(obj1.r+obj2.r)**2)
    dt   = -(((dvdr)+((d)**0.5))/(dvdv))
    return( dt )

def cambio_de_velocidad_por_choque_entre_particulas(obj1: particula, obj2: particula, dt):
    print(f'            posiciones iniciales de {obj1.idx} es: {obj1.p}, de {obj2.idx} es: {obj2.p}')
    obj1.p = obj1.p - dt*obj1.v
    obj2.p = obj2.p - dt*obj2.v
    print(f'            posiciones finales de {obj1.idx} es: {obj1.p}, de {obj2.idx} es: {obj2.p}')
    deltat = dtt(obj1, obj2)
    print(f'            el tiempo que tarda en llegar a ser tangenciales es: {deltat}')
    obj1.p = obj1.p + deltat*obj1.v
    obj2.p = obj2.p + deltat*obj2.v
    print(f'            posiciones previas al choque: {obj1.p, obj2.p}')
    ### ya tenemos todo cool
    # dr   = obj2.p-obj1.p
    # dv   = obj2.v-obj1.v
    # dvdr = ((dv[0])*(dr[0])) + ((dv[1])*(dr[1]))
    # j = (2*obj1.m*obj2.m*(dvdr))/((obj1.r+obj2.r)*(obj1.m+obj2.m))
    # jx = j * dr[0] / (obj1.r+obj2.r)
    # jy = j * dr[1] / (obj1.r+obj2.r)
    print(f'            velocidades antes de choque de {obj1.idx} es: {obj1.v}, de {obj2.idx} es: {obj2.v}')
    # obj1.v[0] = obj1.v[0] + jx / obj1.m
    # obj1.v[1] = obj1.v[1] + jy / obj1.m
    # obj2.v[0] = obj2.v[0] - jx / obj2.m
    # obj2.v[1] = obj2.v[1] - jy / obj2.m
    sigma = obj1.m + obj2.m
    num1 = np.dot(obj1.v-obj2.v, obj1.p-obj2.p)
    num2 = np.dot(obj2.v-obj1.v, obj2.p-obj1.p)
    obj1.v = obj1.v - (2*obj2.m/(sigma))*((num1)/(dist(obj1.p,obj2.p)**2))*(obj1.p-obj2.p)
    obj2.v = obj2.v - (2*obj1.m/(sigma))*((num2)/(dist(obj2.p,obj1.p)**2))*(obj2.p-obj1.p)
    print(f'            velocidades despues de choque de {obj1.idx} es: {obj1.v}, de {obj2.idx} es: {obj2.v}')
    tiempo_restante = dt - deltat
    obj1.p = obj1.p + tiempo_restante * obj1.v
    obj2.p = obj2.p + tiempo_restante * obj2.v
    print(f'            posiciones corregidas: {obj1.p, obj2.p}')

def cambia_la_posicion(obj1: particula, dt_para_tangencial):
    obj1.p = obj1.p + dt_para_tangencial * obj1.v

def cambio_de_velocidad_por_choque_con_pared(parti: particula,lx,ly):
    if (lx-parti.p[0] < parti.r) and (parti.p[0] > 0):
        parti.v[0] = -parti.v[0]
        print("         ¡CHOQUE CON PARED DERECHA!")
    if (parti.p[0]+lx < parti.r) and (parti.p[0] < 0):
        parti.v[0] = -parti.v[0]
        print("         ¡CHOQUE CON PARED IZQUIERDA!")
    if (ly-parti.p[1] < parti.r) and (parti.p[1] > 0):
        parti.v[1] = -parti.v[1]
        print("         ¡CHOQUE CON TECHO!")
    if (parti.p[1]+ly < parti.r) and (parti.p[1] < 0):
        parti.v[1] = -parti.v[1]   
        print("         ¡CHOQUE CON SUELO!")

def redaccion_de_texto(lista):
    pos = open('posiciones.txt','a')
    vel = open('velocidades.txt','a')
    for i in lista:
        pos.write('('+str(tuple(i.p)[0])+';'+str(tuple(i.p)[1])+';'+str(i.idx)+')'+',')
        vel.write('('+str(tuple(i.v)[0])+';'+str(tuple(i.v)[1])+';'+str(i.idx)+')'+',')
    pos.write('\n')
    vel.write('\n')
    pos.close()
    vel.close()
  


### BPT == Búsqueda de partículas traslapadas

def Arbol2D_BPT(raiz: nodo, punto: particula, L, p = 0, k = 2):
    if raiz is None:    
        return(L)
    eje = p%2
    sb = None
    ob = None
    if punto.p[eje] < raiz.part.p[eje]:
        sb = raiz.i
        ob = raiz.d
    else:
        sb = raiz.d
        ob = raiz.i
    if (dist(raiz.part.p,punto.p)<(raiz.part.r + punto.r)) and ((raiz.part.p != punto.p).any()): #una vez terminado el código implementar aquí el cpálculo de la velocidad final
        L.append(raiz.part)
    
    # Recursion.
    L = Arbol2D_BPT(sb, punto, L, p+1, k=2)
    if punto.r >= abs(raiz.part.p[eje]-punto.p[eje]):
        L = Arbol2D_BPT(ob, punto, L, p+1, k=2)
    return(L)

class experimento():
    def __init__(self, lista_de_particulas, lx, ly):
        self.lx, self.ly = lx, ly
        self.lp = lista_de_particulas
    def realiza_el_experimento(self, num_de_pasos, dt):
        self.dt = dt
        for i in range(num_de_pasos):
            arbol = Arbol2D(self.lp, 0)
            print(f'tiempo: {i}')
            ### El siguiente es un 
            for j in self.lp:
                print(f'    +partícula: {j.idx} ||| con posicion {j.p} ||| con velocidad: {j.v}')
                #lista particulas que chocan con j, nota que no uso la lsita pero puede servir para saber con cuantas partículas choca en un mismo tiempo
                listapqchcj = Arbol2D_BPT(arbol,j,[])
                for k in listapqchcj:
                    print(f'        ++ Lista de particulas que chocan: {[(i.p,i.idx) for i in listapqchcj]}')
                    cambio_de_velocidad_por_choque_entre_particulas(j,k,self.dt)
                cambio_de_velocidad_por_choque_con_pared(j, self.lx, self.ly)
            #despues de todos los cambios por colisiones redacto el csv
            redaccion_de_texto(self.lp)
            for k in self.lp:
                k.p = k.p + self.dt*k.v   ### aqui solo cambio las posiciones con las posiciones debidas a un potencial!!!! ueuwuwuwuwuwuuwuwuwuw
                
