import numpy as np
import vpython as vp
from numpy import random as rand

##caja cuadrada:

#longi_cuadrado = float(input('dame la longitud del cuadrado \n'))
#x_i = float(input('dame la posicion inicial en x de la partícula \n'))
#y_i = float(input('dame la posicion inicial en x de la partícula \n'))
#z_i = float(input('dame la posicion inicial en x de la partícula \n'))
#v_x_i = float(input('dame la posicion inicial en x de la partícula \n'))
#v_y_i = float(input('dame la posicion inicial en x de la partícula \n'))
#v_z_i = float(input('dame la posicion inicial en x de la partícula \n'))

#pos_i = vp.vector(x_i,y_i,z_i)
#vel_i = vp.vector(v_x_i, v_y_i, v_z_i)

#t = 0
#dt = 0.01

#particula = vp.sphere(pos = pos_i, radius = 0.2)
#trail = vp.curve(color = vp.vector(1,0,0))

#vp.scene.autoscale = False

#while t<10:
 #   vp.rate(250)
  #  trail.append(pos = particula.pos)
   # pos_t = pos_i + dt * vel_i
    ###rebote pared sobre cuadrado.
    #if pos_t.x > longi_cuadrado: #agregar + radio
     #   extra = pos_t.x - longi_cuadrado
      #  pos_t.x = pos_t.x - 2*(extra)
       # vel_i.x = -vel_i.x
    #elif pos_t.x < 0: #agregar + radio
     #   pos_t.x = pos_t.x + 2*(np.abs(pos_t.x))
      #  vel_i.x = -vel_i.x
    #if pos_t.y > longi_cuadrado: #agregar + radio
     #   extra = pos_t.y - longi_cuadrado
      #  pos_t.y = pos_t.y - 2*(extra)
       # vel_i.y = -vel_i.y
    #elif pos_t.y < 0: #agregar + radio
     #   pos_t.y = pos_t.y + 2*(np.abs(pos_t.y))
      #  vel_i.y = -vel_i.y
    #if pos_t.z > longi_cuadrado: #agregar + radio
     #   extra = pos_t.z - longi_cuadrado
      #  pos_t.z = pos_t.z - 2*(extra)
       # vel_i.z = -vel_i.z
    #elif pos_t.z < 0: #agregar + radio
     #   pos_t.z = pos_t.z + 2*(np.abs(pos_t.z))
      #  vel_i.z = -vel_i.z
    ###actualizacion
    #particula.pos = pos_t
    #pos_i = pos_t
    #t = t + dt

## fin caja cuadrada.

## caja circular:

puntos_de_choque = []
def chicharron_ext(p_0, v_0, r):
  b = 2*(vp.dot(p_0,v_0))
  c = (vp.mag(p_0))**2-r**2
  a = (vp.mag(v_0))**2
  t = (-b+np.sqrt((b**2)-(4*a*c)))/(2*a)
  return(t)
def chicharron_int(p_0, v_0, r):
  b = 2*(vp.dot(p_0,v_0))
  c = (vp.mag(p_0))**2-r**2
  a = (vp.mag(v_0))**2
  t = (-b-np.sqrt((b**2)-(4*a*c)))/(2*a)
  return(t)
def redireccion(v_0, normal):
  v_f = v_0-2*(vp.dot(v_0, normal))*normal
  return(v_f)
def rebote_ext(obj, radio_ext, dt):
    if vp.mag(obj.pos) > radio_ext:
      ##calculo de t, tq hace que ||v||^2 = r^2
      t = chicharron_ext(obj.pos, obj.vel, radio_ext)
      ##vector de la intersección:
      vect_inter = obj.pos + t*obj.vel
      ##calculo del vector normal:
      normal = -(vp.hat(vect_inter))
      ##calculo el nuevo vector velocidad dado el choque:
      v_f = redireccion(obj.vel, normal)
      ##calculo nuevo vector posición:
      obj.pos = vect_inter + dt*v_f
      ##actualizo el vector posicion inicial y vector velocidad: 
      obj.vel = v_f
      obj.pos_0 = vect_inter
def rebote_int(obj, radio_int, dt):
    if vp.mag(obj.pos) < radio_int:
      ##calculo de t, tq hace que ||v||^2 = r^2
      t = chicharron_int(obj.pos, obj.vel, radio_int)
      ##vector de la intersección:
      vect_inter = obj.pos + t*obj.vel
      ##calculo del vector normal:
      normal = vp.hat(vect_inter)
      ##calculo el nuevo vector velocidad dado el choque:
      v_f = redireccion(obj.vel, normal)
      ##calculo nuevo vector posición:
      obj.pos = vect_inter + dt*v_f
      ##actualizo el vector posicion inicial y vector velocidad: 
      obj.vel = v_f
      obj.pos_0 = vect_inter

            


p_0 = vp.vector(-1,0,0) #<- se puede cambiar posicion inicial
v = vp.vector(1,1,0)    #<- se puede cambiar velocidad inicial
particula = vp.sphere(pos = p_0, radius = 0.25) #<- se puede cambiar el radio
vp.ring(pos=vp.vector(0,0,0),
             axis=vp.vector(0,0,1),
             radius=25, thickness=0.1) #<- debe cambiar el radio si cambia el radio arriba este es el exterior
vp.ring(pos=vp.vector(0,0,0),
             axis=vp.vector(0,0,1),
             radius=10, thickness=0.1) #<- debe cambiar el radio si cambia el radio arriba este es el interior


particula.vel = v 
#particula.pos_0 = p_0 <- checar notas de pelota_caja_circular
camino = vp.curve(color = vp.vector(1,0,0))

t = 0
dt = 0.01 #<- se puede cambiar el paso temporal
radio_ext = 25 #<- se puede cambiar condicion exterior de la caja
radio_int = 10 #<- se puede cambiar condicion interior de la caja

while t<1:
    vp.rate(250)
    rebote_ext(particula, radio_ext, dt)
    rebote_int(particula, radio_int, dt)
    particula.pos = particula.pos + dt*particula.vel
    camino.append(pos = particula.pos)
    
# nota: no me salía porque quería cambiar el p_0 de forma directa en el if de las funciones rebotes, es decir, quería re-definir la variable, aun e sun misterio para mi por qué no funcionaba.
# nota_2: cambié la parte de obj.pos_0 por obj.pos ya que en el chicharron porque el código asociado al rebote dependía de donde tomaba como inicio, entonces en el caso donde no habia gravedad
# se cagaba todo porque se tomaba el "path" desde el momento inicial y eso está mal debe ser tomado el cmaino en el momento en el que en el siguiente dt se rebasa la barrera
# esto tiene su razon y es que si lo tomo desde el inicio, se pierde información, por ello hay que hacer una actualizacion tanto en momentos como en velocidades; 
# en las funciones rebote y en la sección del código de la gravedad respectivamente,
# NOTA! ESTAS NOTAS APLICAN PARA:
## -pelota_caja_circular 
## -pelota_caja_circular_con_gravedad
#solo que se me ocurrieron en el momento y no quería qyue s eme olvidaran y por lo tanto lo dejé en un archivo!
