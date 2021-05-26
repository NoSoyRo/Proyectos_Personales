from manimlib.imports import *
g= 0.5
l = 1
def f(x):
    return(np.array([x[1], -(g/l)*np.sin(x[0]),0]))
class p_d_e(Scene):
    CONFIG = {"rate_func": there_and_back}
    def construct(self):
        self.ef()
    def ef(self):
        a = StreamLines(func = f)
        self.play(ShowCreation(a))
        self.add(AnimatedStreamLines(StreamLines(func = f)))
        self.wait(10)

n_it = 1

class fractal(Scene):
    def construct(self):
        self.dibujo()
    def dibujo(self):
        L = []
        l_1 = Line(start = 0.5*UP + 0.5*LEFT, end = 0.5*UP +0.5*RIGHT)
        l_2 = Line(start = 0.5*UP + 0.5*LEFT, end = -0.5*UP +0.5*LEFT)
        L.append([l_1,l_2])
        gpo_0 = VGroup(l_1,l_2)
        self.play(Write(gpo_0))
        for i in range(n_it):
            L_i = []
            for j in L[-1]:
                L_i.append(j.copy())
            for k in L_i:
                L_i.append(k.copy())
            gpo_rot = VGroup(*L_i)
            self.play(Write(gpo_rot))
            self.wait()
            self.play(gpo_rot.rotate, PI/2, {"about_point":0.5*RIGHT + 0.5*UP})
            self.wait()
            L.append(L_i)
