from numpy import *

from manimlib.imports import *

m_1 = 4
m_2 = 0.8
k = 4
l_0 = 3
t_f = 20 # tiempo final de solucion
n_e = 800 # cantidad de pasos en la particion
x1_0 = -1
vx1_0 = 0.3
y1_0 = 0
vy1_0 = 0.4
x2_0 = 1
vx2_0 = 0 
y2_0 = 0
vy2_0 = 0

def RK_4(edo,x_ini,t):
    sol = zeros( (len(t) , len(x_ini)) )
    sol[0,:] = x_ini
    delta = t[1]-t[0]
    for i in range(0,len(t)-1):
        k1 = edo(sol[i,:],t[i])
        k2 = edo(sol[i,:] + 0.5*delta*k1 , t[i] + 0.5*delta)
        k3 = edo(sol[i,:] + 0.5*delta*k2 , t[i] + 0.5*delta)
        k4 = edo(sol[i,:] + delta*k2 , t[i] + delta)
        sol[i+1,:] = sol[i,:] + (delta/6.0)*(k1 + 2.0*k2 + 2.0*k3 + k4)
    return sol

def edo_b_mmr(arr,t):
    # [x1,vx1,y1,vy1,x2,vx2,y2,vy2]
    x1,vx1,y1,vy1,x2,vx2,y2,vy2 = arr[0],arr[1],arr[2],arr[3],arr[4],arr[5],arr[6],arr[7]
    d12  = np.sqrt((x2-x1)**2+(y2-y1)**2)
    d12x = (x2-x1)
    d12y = (y2-y1)
    
    dx1  = vx1
    dy1  = vy1
    dx2  = vx2
    dy2  = vy2
    dvx1 = -(k/m_1)*((2*(l_0-d12)*(d12x))/(d12))
    dvy1 = -(k/m_1)*((2*(l_0-d12)*(d12y))/(d12))
    dvx2 = (k/m_2)*((2*(l_0-d12)*(d12x))/(d12))
    dvy2 = (k/m_2)*((2*(l_0-d12)*(d12y))/(d12))
    
    return(np.array([dx1,dvx1,dy1,dvy1,dx2,dvx2,dy2,dvy2]))

t = np.linspace(0,t_f,n_e)
x_ini = np.array([x1_0,vx1_0,y1_0,vy1_0,
                  x2_0,vx2_0,y2_0,vy2_0])
sol = RK_4(edo_b_mmr,x_ini,t)

X_1 = [i for i in sol[:,0]]
Y_1 = [i for i in sol[:,2]]
X_2 = [i for i in sol[:,4]]
Y_2 = [i for i in sol[:,6]]
X_cm = [(m_1/(m_1+m_2))*i+(m_2/(m_1+m_2))*j for i,j in zip(X_1,X_2)]
Y_cm = [(m_1/(m_1+m_2))*i+(m_2/(m_1+m_2))*j for i,j in zip(Y_1,Y_2)]


class Grid(VGroup):
    CONFIG = {
        "height": 6.0,
        "width": 6.0,
    }

    def __init__(self, rows, columns, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)

        x_step = self.width / self.columns
        y_step = self.height / self.rows

        for x in np.arange(0, self.width + x_step, x_step):
            self.add(Line(
                [x - self.width / 2., -self.height / 2., 0],
                [x - self.width / 2., self.height / 2., 0],
            ))
        for y in np.arange(0, self.height + y_step, y_step):
            self.add(Line(
                [-self.width / 2., y - self.height / 2., 0],
                [self.width / 2., y - self.height / 2., 0]
            ))

class ScreenGrid(VGroup):
    CONFIG = {
        "rows": 8,
        "columns": 14,
        "height": FRAME_Y_RADIUS * 2,
        "width": 14,
        "grid_stroke": 0.5,
        "grid_color": WHITE,
        "axis_color": RED,
        "axis_stroke": 2,
        "labels_scale": 0.25,
        "labels_buff": 0,
        "number_decimals": 2
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        rows = self.rows
        columns = self.columns
        grid = Grid(width=self.width, height=self.height, rows=rows, columns=columns)
        grid.set_stroke(self.grid_color, self.grid_stroke)

        vector_ii = ORIGIN + np.array((- self.width / 2, - self.height / 2, 0))
        vector_si = ORIGIN + np.array((- self.width / 2, self.height / 2, 0))
        vector_sd = ORIGIN + np.array((self.width / 2, self.height / 2, 0))

        axes_x = Line(LEFT * self.width / 2, RIGHT * self.width / 2)
        axes_y = Line(DOWN * self.height / 2, UP * self.height / 2)

        axes = VGroup(axes_x, axes_y).set_stroke(self.axis_color, self.axis_stroke)

        divisions_x = self.width / columns
        divisions_y = self.height / rows

        directions_buff_x = [UP, DOWN]
        directions_buff_y = [RIGHT, LEFT]
        dd_buff = [directions_buff_x, directions_buff_y]
        vectors_init_x = [vector_ii, vector_si]
        vectors_init_y = [vector_si, vector_sd]
        vectors_init = [vectors_init_x, vectors_init_y]
        divisions = [divisions_x, divisions_y]
        orientations = [RIGHT, DOWN]
        labels = VGroup()
        set_changes = zip([columns, rows], divisions, orientations, [0, 1], vectors_init, dd_buff)
        for c_and_r, division, orientation, coord, vi_c, d_buff in set_changes:
            for i in range(1, c_and_r):
                for v_i, directions_buff in zip(vi_c, d_buff):
                    ubication = v_i + orientation * division * i
                    coord_point = round(ubication[coord], self.number_decimals)
                    label = Text(f"{coord_point}",font="Arial",stroke_width=0).scale(self.labels_scale)
                    label.next_to(ubication, directions_buff, buff=self.labels_buff)
                    labels.add(label)

        self.add(grid, axes, labels)


class a_dmr(Scene):
    def construct(self):
        #self.planteamiento()
        self.ejes()
        self.animacion()
    def planteamiento(self):
        titulo = TextMobject("""Sistema de dos masas unidas por un resorte de \n
                                constante de elasticidad: $k$ y longitud natural $l_0$, \n
                                donde las masas tienen una volicidad inicial y una posicion inicial.""")
        titulo.cont = SurroundingRectangle(titulo,color=YELLOW,fill_color=BLACK, fill_opacity=10)
        gpo_tit = VGroup(titulo.cont,titulo).scale(0.7)
        expli = TextMobject(""" Supongamos dos masas ($m_1, m_2$) \n
                                unidas por un resorte con coficiente \n
                                de elasticidad $k$ y longitud natural $l_0$. """).move_to(np.array([2,0,0]))
        expli.cont = SurroundingRectangle(expli,color=YELLOW,fill_color=BLACK, fill_opacity=10)
        gpo_expli = VGroup(expli.cont,expli)
        d_1 = Dot(point = np.array([-5,-3,0]), radius = .3, color = RED)
        d_2 = Dot(point = np.array([-3,2,0]), radius = .3, color = RED)
        dl = DashedLine(start = d_1.get_center(), end = d_2.get_center(), buff = 0)
        conexion = TextMobject("""No es complicado ver que la \n
                                  energía cinética y potencial, total \n
                                  son: 
                                  $$K = \\dfrac{1}{2}(m_1(\\dot{x}_1^2+\\dot{y}_1^2)+m_2(\\dot{x}_2^2+\\dot{y}_2^2))$$
                                  $$U = k(l_0-\\sqrt{(x_2-x_1)^2+(y_2-y_1)^2})^2$$
                                  """).move_to(np.array([2,0,0]))
        conexion.bg = SurroundingRectangle(conexion,color=YELLOW,fill_color=BLACK, fill_opacity=10)
        gpo_cone = VGroup(conexion.bg,conexion)
        fin = TextMobject(""" De este modo, podemos obtener un sistema de ecuaciones \n
                              altamente no lineal usando el formalismo lagrangiano que \n
                              si resolvemos numéricamente, se puede obtener una aproximación \n
                              al comportamiento del sistema como se muestra a continuación para \n
                              unas velocidades y posiciones iniciales dadas.""")
        fin.bg = SurroundingRectangle(fin, color = YELLOW, fill_color = BLACK, fill_opacity = 10)
        gpo_fin = VGroup(fin.bg, fin).scale(0.7)
        #animamos:
        self.play(Write(gpo_tit))
        self.wait(6)
        self.play(Write(dl),Write(d_1),Write(d_2),ReplacementTransform(gpo_tit,gpo_expli))
        self.wait(6)
        self.play(ReplacementTransform(gpo_expli,gpo_cone))
        self.wait(6)
        self.play(FadeOut(dl),FadeOut(d_1),FadeOut(d_2),ReplacementTransform(gpo_cone, gpo_fin))
        self.wait(15)
        self.play(FadeOut(gpo_fin))
        self.wait()
    def ejes(self):
        grid = ScreenGrid()
        self.play(Write(grid))
    def animacion(self):
        x_1 = np.array([x_ini[0]*np.cos(x_ini[2]),
                        x_ini[0]*np.sin(x_ini[2]),
                        0])
        x_2 = np.array([x_ini[4]*np.cos(x_ini[6]),
                        x_ini[4]*np.sin(x_ini[6]),
                        0])
        #d_1 = Dot(point = x_1)
        #d_2 = Dot(point = x_2)
        #self.add(d_1,d_2)
        #self.wait()
        D_1 = []
        D_2 = []
        D_cm= []
        res = []
        #D_1.append(d_1)
        #D_2.append(d_2)
        for i,j,k,l,m,n in zip(X_1,Y_1,X_2,Y_2,X_cm,Y_cm):
            d_i_1 = Dot(point = np.array([i,j,0]), radius = 0.3, color = RED)
            d_i_2 = Dot(point = np.array([k,l,0]), radius = 0.3, color = RED)
            res_i = DashedLine(start = d_i_1.get_center(),
                    end = d_i_2.get_center()
                       )
            d_i_cm = Dot(point = np.array([m,n,0]), radius = 0.02, color = YELLOW)
            D_1.append(d_i_1)
            D_2.append(d_i_2)
            res.append(res_i)
            D_cm.append(d_i_cm)
        D_1_VG = VGroup(*D_1)
        D_2_VG = VGroup(*D_2)
        res_VG = VGroup(*res)
        cm_VG  = VGroup(*D_cm)
        texto = TextMobject("Centro de masa")
        texto.bg = SurroundingRectangle(texto, color = YELLOW, fill_color = BLACK, fill_opacity = 10)
        gpo_texto = VGroup(texto.bg, texto).move_to(np.array([-5,3,0]))
        pto = Dot(color = YELLOW, radius = 0.02).next_to(gpo_texto, LEFT, buff = 0.1)
        self.play(ShowIncreasingSubsets(cm_VG),ShowSubmobjectsOneByOne(res_VG),ShowSubmobjectsOneByOne(D_1_VG),
        ShowSubmobjectsOneByOne(D_2_VG)
        , run_time = 5, rate_func = linear)
        
