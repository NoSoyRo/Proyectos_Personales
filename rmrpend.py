from numpy import *
import numpy as np
from manimlib.imports import *

def RK_4(edo, x_ini, t):
    sol = zeros((len(t), len(x_ini)))
    sol[0, :] = x_ini
    delta = t[1]-t[0]
    for i in range(0, len(t)-1):
        k1 = edo(sol[i, :], t[i])
        k2 = edo(sol[i, :] + 0.5*delta*k1, t[i] + 0.5*delta)
        k3 = edo(sol[i, :] + 0.5*delta*k2, t[i] + 0.5*delta)
        k4 = edo(sol[i, :] + delta*k2, t[i] + delta)
        sol[i+1, :] = sol[i, :] + (delta/6.0)*(k1 + 2.0*k2 + 2.0*k3 + k4)
    return sol


m_1 = 1
m_2 = 0.1
k = 0.5
b = 1.5
g = 3.867
tf = 10
nt = 400
x_0, th_0, vx_0, vth_0 = 0,np.pi+0.1,1,-1


def edo_sf(x_ini, t):
    #x_ini = [x2,theta,vx2,vtheta]
    x2 = x_ini[0]
    th = x_ini[1]
    vx2 = x_ini[2]
    vth = x_ini[3]
    #ecuaciones
    dth = vth
    dx2 = vx2
    # calculos para dvtheta:
    A_1 = (m_1*b*cos(th)*2*k*x2)/(m_1+m_2)
    A_2 = m_1*vx2*vth*b*sin(th)
    A_3 = -m_1*b*(g+vx2*vth)*sin(th)
    A_4 = -((m_1*b*cos(th))/(m_1*m_2))*m_1*b*vth**2*sin(th)
    c_1 = m_1*b**2-((m_1**2*b**2*cos(th)**2)/(m_1+m_2))
    dvth = (1/c_1)*(A_1+A_2+A_3+A_4)
    #calculos para dvx2:
    B_1 = m_1*vx2*vth*b*sin(th)
    B_2 = ((m_1*b**2)/(m_1*b*cos(th)))*2*k*x2
    B_3 = -((m_1*b**2)/(m_1*b*cos(th)))*m_1*b*vth**2*sin(th)
    B_4 = -m_1*b*(g+vx2*vth)*sin(th)
    c_2 = m_1*cos(th)*b-((m_1*(m_1+m_2)*b**2)/(m_1*b*cos(th)))
    dvx2 = (1/c_2)*(B_1+B_2+B_3+B_4)
    return(np.array([dx2, dth, dvx2, dvth]))


t = linspace(0, tf, nt)
x_ini = [x_0, th_0, vx_0, vth_0]  # [X,TH,VX,VTH]
sol = RK_4(edo_sf, x_ini, t)

y_1real = [-b*cos(th) for th in sol[:, 1]]
x_1real = [x2+b*sin(th) for th,x2 in zip(sol[:, 1], sol[:, 0])]
y_2real = [0 for x2 in sol[:, 0]]
x_2real = [x2 for x2 in sol[:, 0]]


v_maxx2, v_minx2, v_th_max, v_th_min = max(sol[:,2]), min(sol[:,2]), max(sol[:,3]), min(sol[:,3])
Vs = [v_maxx2, v_minx2, v_th_max, v_th_min]
ymax, ymin = max(Vs), min(Vs)

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
        grid = Grid(width=self.width, height=self.height,
                    rows=rows, columns=columns)
        grid.set_stroke(self.grid_color, self.grid_stroke)

        vector_ii = ORIGIN + np.array((- self.width / 2, - self.height / 2, 0))
        vector_si = ORIGIN + np.array((- self.width / 2, self.height / 2, 0))
        vector_sd = ORIGIN + np.array((self.width / 2, self.height / 2, 0))

        axes_x = Line(LEFT * self.width / 2, RIGHT * self.width / 2)
        axes_y = Line(DOWN * self.height / 2, UP * self.height / 2)

        axes = VGroup(axes_x, axes_y).set_stroke(
            self.axis_color, self.axis_stroke)

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
        set_changes = zip([columns, rows], divisions, orientations, [
                          0, 1], vectors_init, dd_buff)
        for c_and_r, division, orientation, coord, vi_c, d_buff in set_changes:
            for i in range(1, c_and_r):
                for v_i, directions_buff in zip(vi_c, d_buff):
                    ubication = v_i + orientation * division * i
                    coord_point = round(ubication[coord], self.number_decimals)
                    label = Text(f"{coord_point}", font="Arial",
                                 stroke_width=0).scale(self.labels_scale)
                    label.next_to(ubication, directions_buff,
                                  buff=self.labels_buff)
                    labels.add(label)

        self.add(grid, axes, labels)


class rmrpend(GraphScene):
    CONFIG={
        "x_min": -1,
        "x_max": tf + 1,
        "y_min": -10,
        "y_max": 10,
        "graph_origin": 2 * UP + 3 * LEFT,
        "y_axis_height": 3,
        "x_axis_width": 8,
        "x_axis_label": "$t$",
        "y_axis_label": "$\\theta(t), x(t)$"
    }
    def construct(self):
        self.animacion()
        

    def animacion(self):
        self.play(Write(Dot(point=np.array([-3, 0, 0]))), Write(Dot(point=np.array([3, 0, 0]))))
        M_1 = []
        M_2 = []
        R_1 = []
        R_2 = []
        PEN = []
        self.setup_axes(animate=True)
        grafica_x2 = VGroup(*[Dot( radius = 0.03, color = GREEN).move_to(self.coords_to_point(t,x)) for x,t in zip(x_2real,t)])
        grafica_th = VGroup(*[Dot( radius = 0.03, color = BLUE).move_to(self.coords_to_point(t,th)) for th,t in zip(sol[:,1],t)])

        #para agregar las velocidades: ajusta tamaños
        ###################################################################################################################
        #self.y_min = ymin
        #self.y_max = ymax
        #self.graph_origin = 1 * UP + 2 * RIGHT
        #self.y_axis_height = 3
        #self.setup_axes(animate=True)
        
        #grafica_vx2 = VGroup(*[Dot( radius = 0.05).move_to(self.coords_to_point(t,vx2)) for vx2,t in zip(sol[:,2],t)])
        #grafica_vth = VGroup(*[Dot( radius = 0.05).move_to(self.coords_to_point(t,vth)) for vth,t in zip(sol[:,3],t)])
        ###################################################################################################################
        
        #simulacion
        for i,j,k,l in zip(x_1real,y_1real,x_2real,y_2real):
            M_1_o_i = Dot(point = np.array([i,j,0]), radius = 0.1, color = YELLOW)
            M_2_o_i = Dot(point = np.array([k,l,0]), radius = 0.1, color = ORANGE)
            R_1_o_i = DashedLine(start = np.array([-3,0,0]),end = M_2_o_i.get_center(), color = RED)
            R_2_o_i = DashedLine(start=M_2_o_i.get_center(), end=np.array([3,0,0]), color = BLUE)
            pend    = Line(start=M_2_o_i.get_center(), end=M_1_o_i.get_center(),color = GOLD)
            M_1.append(M_1_o_i)
            M_2.append(M_2_o_i)
            R_1.append(R_1_o_i)
            R_2.append(R_2_o_i)
            PEN.append(pend)
        


        M_1vg = VGroup(*M_1)
        M_2vg = VGroup(*M_2)
        R_1vg = VGroup(*R_1)
        R_2vg = VGroup(*R_2)
        PENvg = VGroup(*PEN)

        p_1,l_1,p_2,l_2 = Dot(color=GREEN).move_to(np.array([-5, 1, 0])), TexMobject("x").move_to(np.array([-4.7, 1, 0])), Dot(color=BLUE).move_to(np.array([-5, 0.5, 0])), TexMobject("\\theta").move_to(np.array([-4.7, 0.5, 0]))
        origen = Line(start = np.array([0,0.35,0]), end = np.array([0,-0.35,0]))
        ori_tex = TexMobject("\\mathcal{O}").next_to(origen, DOWN, buff = 0.1)
        self.play(Write(p_1),Write(l_1),Write(p_2),Write(l_2), Write(origen), Write(ori_tex))
        self.wait()
        self.play(ShowSubmobjectsOneByOne(R_1vg),
                  ShowSubmobjectsOneByOne(R_2vg), 
                  ShowSubmobjectsOneByOne(PENvg), 
                  ShowSubmobjectsOneByOne(M_1vg),
                  ShowSubmobjectsOneByOne(M_2vg),
                  ShowIncreasingSubsets(grafica_x2),
                  ShowIncreasingSubsets(grafica_th),
                  #ShowIncreasingSubsets(grafica_vx2),
                  #ShowIncreasingSubsets(grafica_vth),
                  run_time=8, rate_func=linear)
