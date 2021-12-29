import numpy as np
import matplotlib.pyplot as plt 
from numpy import random as rand
from numpy import linalg as lng 
import vpython as vp

class p():
    def __init__(self, p_ini, v_ini, m, r):
        self.v = v_ini
        self.p = p_ini
        self.m = m
        self.r = r
        self.dt_techo     = float('inf')
        self.dt_suelo     = float('inf')
        self.dt_paredizq  = float('inf')
        self.dt_paredder  = float('inf')
    def dts_particulas(self, lista): 
        self.dt_particula = [0 for i in lista]

def traslape_deteccion(part, lista):
    pos = part.p
    for i in lista:
        if (lng.norm(i.p-pos)<(i.r+part.r)):
            i,j = lista.index(i)+1, lista.index(i)
            #print("traslape entre %i y %i" %(i,j)) <--- Agregar si quiero corroborar traslapes
            return(True)
    return(False)

def grafica_en_mpl(L,lx,ly):
    radio = L[0].r 
    plt.figure()
    pos = []
    plt.xlim(-lx-1,lx+1)
    plt.ylim(-ly-1,ly+1)
    lin_arriba_y = [ly for i in range(100)]
    lin_arriba_x = [i for i in np.linspace(-lx,lx,100)]
    lin_abajo_y = [-ly for i in range(100)]
    lin_abajo_x = [i for i in np.linspace(-lx,lx,100)]
    lin_izq_x = [-lx for i in range(100)]
    lin_izq_y = [i for i in np.linspace(-lx,lx,100)]
    lin_der_x = [lx for i in range(100)]
    lin_der_y = [i for i in np.linspace(-lx,lx,100)]
    for i in L:
        pos.append([i.p[0],i.p[1]])
        circle1=plt.Circle((i.p[0], i.p[1]), radio, color=[0,0,0])
        plt.gcf().gca().add_artist(circle1)
    plt.plot(lin_arriba_x,lin_arriba_y)
    plt.plot(lin_abajo_x,lin_abajo_y)
    plt.plot(lin_der_x,lin_der_y)
    plt.plot(lin_izq_x,lin_izq_y)
    plt.show()

def grafica_en_vpython(prueba):
    for i in prueba:
        sp_i = vp.sphere(pos = vp.vector(i.p[0],i.p[1],0), radius = .1)

def error_de_cantidades(lx,ly,N,r):
    if (4*lx*ly > N*np.pi*r**2):
        print("Si se puede construir las partículas no traslapadas.")
        return(True)
    else:
        print("No se puede crear las partículas no traslapadas.")
        return(False)

def checa_si_se_sale_alguna(lista,lx,ly):
    r = lista[0].r
    for i in lista:
        if i.p[0]+r > lx:
            print("ta mal en x")
        
        if i.p[0]-r < -lx:
            print("ta mal en x")
        
        if i.p[1]+r > ly:
            print("ta mal en y")
        
        if i.p[1]-r < -ly:
            print("ta mal en y")

def gen_n_parts(num_parts, lx, ly, vx, vy, m, r):
    masa, radio = m,r   #<--- Esto lo puedo cambiar para que el usuario de las masas y radios.
    listax = np.linspace(-lx+radio,lx-radio,1000)
    listay = np.linspace(-ly+radio,ly-radio,1000)
    listavx = np.linspace(-vx,vx,1000)
    listavy = np.linspace(-vy,vy,1000)
    Particulas = []
    #checamos si se puede o nel
    if error_de_cantidades(lx,ly,num_parts,r):
        for i in range(num_parts):
            x,y = rand.choice(listax),rand.choice(listay)
            vx,vy = rand.choice(listavx),rand.choice(listavy)
            p_i_ini = np.array([x,y])
            v_i_ini = np.array([vx,vy])
            p_i = p(p_i_ini,v_i_ini,masa,radio)
            #aqui agregar la funcion traslape 
            while traslape_deteccion(p_i, Particulas):
                x,y = rand.choice(listax),rand.choice(listay)
                p_i_ini = np.array([x,y])
                p_i.p = p_i_ini
            Particulas.append(p_i)
        return(Particulas)
    else:
        print("No se pueden crear las partículas no traslapadas.")
##########hasta aqui todo bien

def dt_pi_pj(part_1,part_2):
    RADIO = part_1.r+part_2.r
    dv   = part_2.v-part_1.v  
    dr   = part_2.p-part_1.p       
    dvdv = (dv[0])**2+(dv[1])**2
    drdr = (dr[0])**2+(dr[1])**2
    dvdr = (dv[0])*(dr[0])+(dv[1])*(dr[1])
    d    = (dvdr)**2-(dvdv)*(drdr-RADIO**2)
    if dvdr >= 0:
        return(float('inf'))
    if d < 0:
        return(float('inf'))
    else:
        return(-((dvdr)+np.sqrt(d))/((dvdv)))
        
def calculo_dts_a_evento_i(lista_de_parts, lx, ly):
    for i in lista_de_parts:
        i.dts_particulas(lista_de_parts)
    #calculo de dt´s de paredes. si true entonces hablamosd e infinito
    for i in lista_de_parts:
        vx,vy,rx,ry,r = i.v[0],i.v[1],i.p[0],i.p[1],i.r
        if vy>0: #vy
            i.dt_techo = (ly-r-ry)/(vy)
            i.dt_suelo = float("inf")
            print(i.dt_techo)
        elif vy<0: #vy
            i.dt_suelo = (-ly+r-ry)/(vy)
            i.dt_techo = float("inf")
            print(i.dt_suelo)
        if vx<0: #vx
            print("uso vx<0")
            i.dt_paredizq = (-lx+r-rx)/(vx)
            i.dt_paredder = float("inf")
            print(rx,i.dt_paredizq)
        elif vx>0: #vx
            print("uso vx>0")
            i.dt_paredder = (lx-r-rx)/(vx)
            i.dt_paredizq = float("inf")
            print(rx,i.dt_paredder)
        if vy == 0:
            i.dt_techo = float('inf')
            i.dt_suelo = float('inf')
        elif vx == 0:
            i.dt_paredder = float('inf')
            i.dt_paredizq = float('inf')
        ind_i = lista_de_parts.index(i)
        for j in lista_de_parts[ind_i:]:
            ind_j = lista_de_parts.index(j)
            dt_ij = dt_pi_pj(i,j)
            i.dt_particula[ind_j] = dt_ij
            lista_de_parts[ind_j].dt_particula[ind_i] = dt_ij

class minimo():
    def __init__(self,valor,de_particula,dpi,dpd,ds,dtch):
        self.valor = valor
        self.dpi = dpi
        self.dpd = dpd
        self.ds  = ds
        self.dtch= dtch
        self.de_particula = de_particula
        

def encuentra_dt_min(lista_de_parts): # dt_part, dpi, dpd, ds, dtch
    dt_minimo_de_cada_particula_objs = []
    dt_minimo_de_cada_particula = []
    for i in lista_de_parts:
        dts_pared_part_i = [i.dt_techo,i.dt_suelo,i.dt_paredder,i.dt_paredizq]
        min_dts_pared_part_i = min(dts_pared_part_i)
        min_dts_parts_part_i = min(i.dt_particula)
        min_tot_i = min([min_dts_pared_part_i,min_dts_parts_part_i])
        if min_tot_i == i.dt_techo:
            minobj = minimo(min_tot_i,False,False,False,False,True)
            print("minimo de techo")
        elif min_tot_i == i.dt_suelo:
            minobj = minimo(min_tot_i,False,False,False,True,False)
            print("minimo de suelo")
        elif min_tot_i == i.dt_paredder:
            minobj = minimo(min_tot_i,False,False,True,False,False)
        elif min_tot_i == i.dt_paredizq:
            minobj = minimo(min_tot_i,False,True,False,False,False)
        elif min_tot_i == min_dts_parts_part_i:
            minobj = minimo(min_tot_i,True,False,False,False,False)
        dt_minimo_de_cada_particula_objs.append(minobj) #<---
        dt_minimo_de_cada_particula.append(minobj.valor)#<---
    minimo_dt_total = min(dt_minimo_de_cada_particula)
    Lista_indicial_de_particulas_con_mismo_minimo_de_dt = []
    i_0 = 0
    for i in range(dt_minimo_de_cada_particula.count(minimo_dt_total)):
        L=dt_minimo_de_cada_particula
        Lista_indicial_de_particulas_con_mismo_minimo_de_dt.append(L.index(minimo_dt_total,i_0))
        i_0+=1
    return(dt_minimo_de_cada_particula_objs,minimo_dt_total,Lista_indicial_de_particulas_con_mismo_minimo_de_dt)

def cambio_de_velocidad_por_choque_entre_particulas(obj1,obj2):
    drx = obj2.p[0]-obj1.p[0]
    dry = obj2.p[1]-obj1.p[1]
    sigma = obj1.r+obj2.r
    dvdr = (obj2.v[0]-obj1.v[0])*(obj2.p[0]-obj1.p[0])+(obj2.v[1]-obj1.v[1])*(obj2.p[1]-obj1.p[1])
    J = (2*obj1.m*obj2.m*dvdr)/(sigma*(obj1.m+obj2.m))
    Jx = J*drx/sigma
    Jy = J*dry/sigma
    obj1.v[0] = obj1.v[0] + Jx/obj1.m
    obj1.v[1] = obj1.v[1] + Jy/obj1.m
    obj2.v[0] = obj2.v[0] - Jx/obj2.m
    obj2.v[1] = obj2.v[1] - Jy/obj2.m
    
def c_d_v_p_p_i(obj):
    obj.v = np.array([-obj.v[0],obj.v[1]])
def c_d_v_p_p_d(obj):
    obj.v = np.array([-obj.v[0],obj.v[1]])
def c_d_v_p_p_s(obj):
    obj.v = np.array([obj.v[0],-obj.v[1]])
def c_d_v_p_p_t(obj):
    obj.v = np.array([obj.v[0],-obj.v[1]])

def dinamica(nparts,lx,ly,vx,vy,m,r,tf):
    Particulas = gen_n_parts(nparts,lx,ly,vx,vy,m,r)
    #Particulas = [p(np.array([0,0]),np.array([1,0]),1,1)]
    global t
    global dta 
    t = 0
    dta = 1
    X = []
    Y = []
    T = []
    while t<tf:
        calculo_dts_a_evento_i(Particulas,lx,ly)
        L1,mindt,L3 = encuentra_dt_min(Particulas)
        t_0 = t + mindt
        print(t_0, mindt)
        while t<t_0:
            for i in Particulas:
                i.p = i.p + dta*i.v
                X.append(i.p[0])
                Y.append(i.p[1])
            t+=dta
            #print(t)
            T.append(t)
        #print(L3)
        for i in L3:
            if L1[i].dpi:
                print("de pared izq")
                c_d_v_p_p_i(Particulas[i])
            elif L1[i].dpd:
                print("de pared der")
                c_d_v_p_p_d(Particulas[i])
            elif L1[i].ds:
                print("de pared suelo")
                c_d_v_p_p_s(Particulas[i])
            elif L1[i].dtch:
                print("de pared techo")
                c_d_v_p_p_t(Particulas[i])
            elif L1[i].de_particula:
                    cambio_de_velocidad_por_choque_entre_particulas(Particulas[0],Particulas[1])
                    print("de particula")
    return(X,Y,T)

X,Y,T = dinamica(2,5,5,3,3,1,1,100)
plt.plot(X,Y)
plt.show()
plt.plot(T,X)
plt.show()
