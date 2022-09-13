import numpy as np

class particula():
    def __init__(self, m, p, vn, va, r, identificador):
        self.m, self.p, self.vn, self.va, self.r, self.idx = m,p,vn,va,r,identificador
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

#Funcionq ue solo altera la velocidad nueva de la spartículas usando las velocidades antiguas de las partículas.

def cambio_de_velocidad_por_choque_entre_particulas(obj1: particula, obj2: particula):
    vec = (obj2.r+obj1.r)*vunit_12(obj1.p,obj2.p) 
    drx = vec[0] 
    dry = vec[1]
    dvx = obj2.va[0]-obj1.va[0]
    dvy = obj2.va[1]-obj1.va[1]
    sigma = obj1.r+obj2.r
    dvdr = (obj2.va[0]-obj1.va[0])*(drx)+(obj2.va[1]-obj1.va[1])*(dry)
    J = (2*obj1.m*obj2.m*dvdr)/(sigma*(obj1.m+obj2.m))
    Jx = J*drx/sigma
    Jy = J*dry/sigma
    print(f"""              +++ Elementos de la ecuación: \n                  
                                   | drx | {drx} \n
                                   | dry | {dry} \n
                                   | dvx | {dvx} \n
                                   | dvy | {dvy} \n
                                   | sig | {sigma} \n
                                   | dvdr| {dvdr} \n
                                   | J   | {J} \n
                                   | Jx  | {Jx} \n
                                   | Jy  | {Jy} \n""")
    return(np.array([obj1.va[0] + Jx/obj1.m, obj1.va[1] + Jy/obj1.m]))

def cambio_de_velocidad_por_choque_con_pared(parti: particula,lx,ly):
    if (lx-parti.p[0] < parti.r) and (parti.p[0] > 0):
        print('             1: cambié la vel porque: ', (lx-parti.p[0] < parti.r), (parti.p[0] > 0), parti.p[0], lx-parti.p[0], parti.r, lx)
        parti.vn[0] = -parti.vn[0]
    if (parti.p[0]+lx < parti.r) and (parti.p[0] < 0):
        print('             2: cambié la vel porque: ', (parti.p[0]+lx < parti.r), (parti.p[0] < 0), parti.p[0], parti.p[0]-lx, parti.r, lx)
        parti.vn[0] = -parti.vn[0]
        
    if (ly-parti.p[1] < parti.r) and (parti.p[1] > 0):
        print('             3: cambié la vel porque: ', (ly-parti.p[1] < parti.r), (parti.p[1] > 0), parti.p[1], ly-parti.p[1], parti.r, ly)
        parti.vn[1] = -parti.vn[1]
        
    if (parti.p[1]+ly < parti.r) and (parti.p[1] > 0):
        print('             4 :cambié la vel porque: ', (parti.p[1]+ly < parti.r), (parti.p[1] > 0), parti.p[1], parti.p[1]-ly, parti.r, ly)
        parti.vn[1] = -parti.vn[1]   
        

def redaccion_de_texto(lista):
    pos = open('posiciones.txt','a')
    vel = open('velocidades.txt','a')
    for i in lista:
        pos.write('('+str(tuple(i.p)[0])+';'+str(tuple(i.p)[1])+';'+str(i.idx)+')'+',')
        vel.write('('+str(tuple(i.vn)[0])+';'+str(tuple(i.vn)[1])+';'+str(i.idx)+')'+',')
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
    # print(f"""      La distancia es: {dist(raiz.part.p,punto.p)} | la suma de radios: {(raiz.part.r + punto.r)}""")
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
            redaccion_de_texto(self.lp)
            print(f'tiempo: {i}')
            ### El siguiente es un 
            for j in self.lp:
                print(f'    +partícula: {j.idx}', f'||| con velocidad: {j.vn}')
                #lista particulas que chocan con j, nota que no uso la lsita pero puede servir para saber con cuantas partículas choca en un mismo tiempo
                listapqchcj = Arbol2D_BPT(arbol,j,[])
                vel_nueva_j = np.array([0,0])
                for k in listapqchcj:
                    vel_vieja = vel_nueva_j
                    vel_nueva_j = vel_nueva_j + cambio_de_velocidad_por_choque_entre_particulas(j,k)
                    print(f"             +++Velocidad cambiada por colisión: {vel_nueva_j-vel_vieja}")
                if len(listapqchcj) == 0:
                    j.vn = j.va
                else:
                    j.vn = vel_nueva_j
                print(f'         ++la posición de la partícula   {j.idx}: ', j.p, '\n',
                      f'        ++la velocidad de la partícula {j.idx}: ', j.vn, '\n',
                      f'        ++las partículas con las que choca son: ', len(listapqchcj))
                cambio_de_velocidad_por_choque_con_pared(j, self.lx, self.ly)

            for k in self.lp:
                k.va = k.vn
                k.p = k.p + self.dt*k.vn
            
########## TESTEO ##########

# L = [particula(1,np.array((4,3)),np.array((7, 2)),np.array((7, 2)),1), 
#      particula(1,np.array((5,4)),np.array((7, 2)),np.array((7, 2)),1), 
#      particula(1,np.array((4,4)),np.array((7, 2)),np.array((7, 2)),0.5)] 

# arbolito = Arbol2D(L)
# lista = Arbol2D_BPT(arbolito, particula(1,np.array((5,4)),np.array((7, 2)),np.array((7, 2)),1), [])
# print(*lista)
