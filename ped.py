from manimlib.imports import *

def Runge_Kutta_4_ord_sistema(f_1, f_2, f_3, f_4, h, D):
    ###datos:
    theta_1_0 = np.pi/5
    theta_2_0 = np.pi
    v_1_0 = 0
    v_2_0 = 0
    
    ###Listas:
    Thetas_1 = []
    Vel_1 = []
    Thetas_2 = []
    Vel_2 = []
    
    ###funcion:
    for i in D:
        #primer estado:
        k_0 = h*f_1(i, v_1_0, v_2_0, theta_1_0, theta_2_0)
        m_0 = h*f_3(i, v_1_0, v_2_0, theta_1_0, theta_2_0)
        l_0 = h*f_2(i, v_1_0, v_2_0, theta_1_0, theta_2_0)
        n_0 = h*f_4(i, v_1_0, v_2_0, theta_1_0, theta_2_0)
        
        #segundo estado:
        k_1 = h*f_1(i+(1/2)*h, v_1_0+(1/2)*k_0, v_2_0+(1/2)*l_0, theta_1_0+(1/2)*m_0, theta_2_0+(1/2)*n_0)
        l_1 = h*f_2(i+(1/2)*h, v_1_0+(1/2)*k_0, v_2_0+(1/2)*l_0, theta_1_0+(1/2)*m_0, theta_2_0+(1/2)*n_0)
        m_1 = h*f_3(i+(1/2)*h, v_1_0+(1/2)*k_0, v_2_0+(1/2)*l_0, theta_1_0+(1/2)*m_0, theta_2_0+(1/2)*n_0)
        n_1 = h*f_4(i+(1/2)*h, v_1_0+(1/2)*k_0, v_2_0+(1/2)*l_0, theta_1_0+(1/2)*m_0, theta_2_0+(1/2)*n_0)
        
        #tercer estado:
        k_2 = h*f_1(i+(1/2)*h, v_1_0+(1/2)*k_1, v_2_0+(1/2)*l_1, theta_1_0+(1/2)*m_1, theta_2_0+(1/2)*n_1)
        l_2 = h*f_2(i+(1/2)*h, v_1_0+(1/2)*k_1, v_2_0+(1/2)*l_1, theta_1_0+(1/2)*m_1, theta_2_0+(1/2)*n_1)
        m_2 = h*f_3(i+(1/2)*h, v_1_0+(1/2)*k_1, v_2_0+(1/2)*l_1, theta_1_0+(1/2)*m_1, theta_2_0+(1/2)*n_1)
        n_2 = h*f_4(i+(1/2)*h, v_1_0+(1/2)*k_1, v_2_0+(1/2)*l_1, theta_1_0+(1/2)*m_1, theta_2_0+(1/2)*n_1)
        
        #cuarto estado:
        k_3 = h*f_1(i+h, v_1_0+k_2, v_2_0+l_2, theta_1_0+m_2, theta_2_0+n_2)
        l_3 = h*f_2(i+h, v_1_0+k_2, v_2_0+l_2, theta_1_0+m_2, theta_2_0+n_2)
        m_3 = h*f_3(i+h, v_1_0+k_2, v_2_0+l_2, theta_1_0+m_2, theta_2_0+n_2)
        n_3 = h*f_4(i+h, v_1_0+k_2, v_2_0+l_2, theta_1_0+m_2, theta_2_0+n_2)
        
        theta_1_sig = theta_1_0 + (1/6)*(k_0+2*k_1+2*k_2+k_3)
        v_1_sig = v_1_0 + (1/6)*(l_0+2*l_1+2*l_2+l_3)
        theta_2_sig = theta_2_0 + (1/6)*(m_0+2*m_1+2*m_2+m_3)
        v_2_sig = v_2_0 + (1/6)*(n_0+2*n_1+2*n_2+n_3)
        
        #Anexado en listas:
        Thetas_1.append(theta_1_sig)
        Vel_1.append(v_1_sig)
        Thetas_2.append(theta_2_sig)
        Vel_2.append(v_2_sig)
        
        #redefinicion de varibale:
        theta_1_0 = theta_1_sig
        theta_2_0 = theta_2_sig
        v_1_0 = v_1_sig
        v_2_0 = v_2_sig
        
    return([Thetas_1, Thetas_2, Vel_1, Vel_2])

def Runge_Kutta_4_ord_sistema_2(f_1, f_2, f_3, f_4, h, D):
    ###datos:
    theta_1_0 = np.pi/5+0.01
    theta_2_0 = np.pi+0.01
    v_1_0 = 0
    v_2_0 = 0
    
    ###Listas:
    Thetas_1 = []
    Vel_1 = []
    Thetas_2 = []
    Vel_2 = []
    
    ###funcion:
    for i in D:
        #primer estado:
        k_0 = h*f_1(i, v_1_0, v_2_0, theta_1_0, theta_2_0)
        m_0 = h*f_3(i, v_1_0, v_2_0, theta_1_0, theta_2_0)
        l_0 = h*f_2(i, v_1_0, v_2_0, theta_1_0, theta_2_0)
        n_0 = h*f_4(i, v_1_0, v_2_0, theta_1_0, theta_2_0)
        
        #segundo estado:
        k_1 = h*f_1(i+(1/2)*h, v_1_0+(1/2)*k_0, v_2_0+(1/2)*l_0, theta_1_0+(1/2)*m_0, theta_2_0+(1/2)*n_0)
        l_1 = h*f_2(i+(1/2)*h, v_1_0+(1/2)*k_0, v_2_0+(1/2)*l_0, theta_1_0+(1/2)*m_0, theta_2_0+(1/2)*n_0)
        m_1 = h*f_3(i+(1/2)*h, v_1_0+(1/2)*k_0, v_2_0+(1/2)*l_0, theta_1_0+(1/2)*m_0, theta_2_0+(1/2)*n_0)
        n_1 = h*f_4(i+(1/2)*h, v_1_0+(1/2)*k_0, v_2_0+(1/2)*l_0, theta_1_0+(1/2)*m_0, theta_2_0+(1/2)*n_0)
        
        #tercer estado:
        k_2 = h*f_1(i+(1/2)*h, v_1_0+(1/2)*k_1, v_2_0+(1/2)*l_1, theta_1_0+(1/2)*m_1, theta_2_0+(1/2)*n_1)
        l_2 = h*f_2(i+(1/2)*h, v_1_0+(1/2)*k_1, v_2_0+(1/2)*l_1, theta_1_0+(1/2)*m_1, theta_2_0+(1/2)*n_1)
        m_2 = h*f_3(i+(1/2)*h, v_1_0+(1/2)*k_1, v_2_0+(1/2)*l_1, theta_1_0+(1/2)*m_1, theta_2_0+(1/2)*n_1)
        n_2 = h*f_4(i+(1/2)*h, v_1_0+(1/2)*k_1, v_2_0+(1/2)*l_1, theta_1_0+(1/2)*m_1, theta_2_0+(1/2)*n_1)
        
        #cuarto estado:
        k_3 = h*f_1(i+h, v_1_0+k_2, v_2_0+l_2, theta_1_0+m_2, theta_2_0+n_2)
        l_3 = h*f_2(i+h, v_1_0+k_2, v_2_0+l_2, theta_1_0+m_2, theta_2_0+n_2)
        m_3 = h*f_3(i+h, v_1_0+k_2, v_2_0+l_2, theta_1_0+m_2, theta_2_0+n_2)
        n_3 = h*f_4(i+h, v_1_0+k_2, v_2_0+l_2, theta_1_0+m_2, theta_2_0+n_2)
        
        theta_1_sig = theta_1_0 + (1/6)*(k_0+2*k_1+2*k_2+k_3)
        v_1_sig = v_1_0 + (1/6)*(l_0+2*l_1+2*l_2+l_3)
        theta_2_sig = theta_2_0 + (1/6)*(m_0+2*m_1+2*m_2+m_3)
        v_2_sig = v_2_0 + (1/6)*(n_0+2*n_1+2*n_2+n_3)
        
        #Anexado en listas:
        Thetas_1.append(theta_1_sig)
        Vel_1.append(v_1_sig)
        Thetas_2.append(theta_2_sig)
        Vel_2.append(v_2_sig)
        
        #redefinicion de varibale:
        theta_1_0 = theta_1_sig
        theta_2_0 = theta_2_sig
        v_1_0 = v_1_sig
        v_2_0 = v_2_sig
        
    return([Thetas_1, Thetas_2, Vel_1, Vel_2])

def f_1(t, omega_1, omega_2, theta_1, theta_2):
    ###funcion:
    return(omega_1)

def f_2(t, w1, w2, t1, t2):
    ###datos:
    m1 = 2
    m2 = 1
    l1 = 1
    l2 = 0.5
    g=9.8
    
    ###funcion:
    ##numerador:
    numerador_f_2 = (-g*(2*m1+m2)*np.sin(t1))+(-m2*g*np.sin(t1-2*t2))+(-2*np.sin(t1-t2)*m2*(w2**2*l2+w1**2*l1*np.cos(t1-t2)))
    ##denominador:
    denominador_f_2 = l1*(2*m1+m2-m2*np.cos(2*t1-t2))
    return(numerador_f_2/denominador_f_2)
    
def f_3(t, omega_1, omega_2, theta_1, theta_2):
    ###funcion:
    return(omega_2)

def f_4(t, w1, w2, t1, t2):
    ###datos:
    m1 = 2
    m2 = 1
    l1 = 1
    l2 = 0.5
    g=9.8
    
    ###funcion:
    numerador_f_4 = (2*np.sin(t1-t2))*(w1**2*l1*(m1+m2)+g*(m1+m2)*np.cos(t1)+w2**2*l2*m2*np.cos(t1-t2))
    denominador_f_4 = l2*(2*m1+m2-m2*np.cos(2*t1-2*t2))
    return(numerador_f_4/denominador_f_4)

class ped(Scene):
    def construct(self):
        intro_can_1 = TextMobject("NoSoyRo")
        intro_can_1.move_to((-3,2.5,0)) \
                   .scale(2)
        self.play(Write(intro_can_1))

        origen = Dot()
        self.play(Write(origen))
        p0_1 = (np.sin(np.pi/5),-np.cos(np.pi/5),0)
        p0_2 = (np.sin(np.pi/5)+0.5*np.sin(np.pi),-np.cos(np.pi/5)-0.5*np.cos(np.pi),0)

        p0_1_otro = (np.sin(np.pi/5+0.01),-np.cos(np.pi/5+0.01),0)
        p0_2_otro = (np.sin(np.pi/5+0.01)+0.5*np.sin(np.pi+0.01),-np.cos(np.pi/5+0.01)-0.5*np.cos(np.pi+0.01),0)

        D = np.linspace(0,20,9000)
        h = D[1]-D[0]

        soluciones = Runge_Kutta_4_ord_sistema(f_1, f_2, f_3, f_4, h, D)

        soluciones_otro = Runge_Kutta_4_ord_sistema_2(f_1, f_2, f_3, f_4, h, D)

        sub_pos_1 = [i for i in soluciones[0][0::40]]
        sub_pos_2 = [i for i in soluciones[1][0::40]]

        sub_pos_1_otro = [i for i in soluciones_otro[0][0::50]]
        sub_pos_2_otro = [i for i in soluciones_otro[1][0::50]]

        linea_1 = Line((0,0,0),(p0_1)) 
        linea_2 = Line((p0_1),(p0_2))

        linea_1_otro = Line((0,0,0),(p0_1_otro)) 
        linea_2_otro = Line((p0_1_otro),(p0_2_otro))

        masa_1 = Dot()
        masa_1.move_to(p0_1)

        masa_2 = Dot()
        masa_2.move_to(p0_2)

        masa_1_otro = Dot()
        masa_1_otro.move_to(p0_1_otro)

        masa_2_otro = Dot()
        masa_2_otro.move_to(p0_2_otro)

        self.play(Write(masa_1), Write(masa_2), Write(linea_1), Write(linea_2), Write(masa_1_otro), Write(masa_2_otro), Write(linea_1_otro), Write(linea_2_otro), )

        for i,j,k,l in zip(sub_pos_1, sub_pos_2, sub_pos_1_otro, sub_pos_2_otro):
            self.remove(masa_1, masa_2, linea_1, linea_2, masa_1_otro, masa_2_otro, linea_1_otro, linea_2_otro)
            masa_i_1 = Dot()
            masa_i_1.set_color(YELLOW)
            masa_i_1.move_to((np.sin(i),-np.cos(i),0))
            masa_i_2 = Dot()
            masa_i_2.set_color(YELLOW)
            masa_i_2.move_to((np.sin(i)+0.5*np.sin(j),-np.cos(i)-0.5*np.cos(j),0))
            linea_i_1 = Line((0,0,0),(masa_i_1.get_center()[0],masa_i_1.get_center()[1],0)) 
            linea_i_2 = Line((masa_i_1.get_center()[0],masa_i_1.get_center()[1],0),(masa_i_2.get_center()[0],masa_i_2.get_center()[1],0))

            masa_i_1_otro = Dot()
            masa_i_1_otro.set_color(YELLOW)
            masa_i_1_otro.move_to((np.sin(k),-np.cos(k),0))
            masa_i_2_otro = Dot()
            masa_i_2_otro.set_color(YELLOW)
            masa_i_2_otro.move_to((np.sin(k)+0.5*np.sin(l),-np.cos(k)-0.5*np.cos(l),0))
            linea_i_1_otro = Line((0,0,0),(masa_i_1_otro.get_center()[0],masa_i_1_otro.get_center()[1],0)) 
            linea_i_2_otro = Line((masa_i_1_otro.get_center()[0],masa_i_1_otro.get_center()[1],0),(masa_i_2_otro.get_center()[0],masa_i_2_otro.get_center()[1],0))
            

            self.add(masa_i_1, masa_i_2, linea_i_1, linea_i_2, masa_i_1_otro, masa_i_2_otro, linea_i_1_otro, linea_i_2_otro)
            masa_1 = masa_i_1
            masa_2 = masa_i_2
            linea_1 = linea_i_1
            linea_2 = linea_i_2
            masa_1_otro = masa_i_1_otro
            masa_2_otro = masa_i_2_otro
            linea_1_otro = linea_i_1_otro
            linea_2_otro = linea_i_2_otro
            self.wait(0.1)
        
g=9.8
l=2

v_0=0
p_0=np.pi/4

D = list(np.linspace(0,20,50000))
h = D[1]-D[0]

vel = []
pos = []

for i in D:
    v_sig = v_0-h*(g/l)*np.sin(p_0)
    p_sig = p_0+h*v_0
    vel.append(v_sig)
    pos.append(p_sig)
    v_0 = v_sig 
    p_0 = p_sig

p_0_red = [i for i in pos[0::200]]

p_0_x = [np.sin(i) for i in p_0_red]
p_0_y = [-np.cos(i) for i in p_0_red]

class p_s(Scene):
    def construct(self):
        intro_can_1 = TextMobject("NoSoyRo")
        intro_can_1.move_to((-3,2.5,0)) \
                   .scale(2)
        self.play(Write(intro_can_1))

        part = Dot()
        part.move_to((p_0_x[0], p_0_y[0],0))\
            .set_color(RED)
        
        self.play(Write(part))

        for i,j in zip(p_0_x, p_0_y):
            self.remove(part)
            part_i = Dot()
            part_i.move_to((i, j,0))
            self.add(part_i)
            self.wait(0.1)
            part = part_i



