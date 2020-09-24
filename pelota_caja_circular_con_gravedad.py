import numpy as np
import vpython as vp
from numpy import random as rand

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
      obj.momento = masa*v_f
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
      obj.momento = masa*v_f

            


p_0 = vp.vector(-10,0,0) #<- se puede cambiar posicion inicial
v = vp.vector(0,0,0)     #<- se puede cambiar velocidad inicial
masa = 5                 #<- se puede cambiar masa de partícula
campo_grav = vp.vector(0,-9.8,0) #<- se puede cambiar gravedad
momento_0 = masa*v

particula = vp.sphere(pos = p_0, radius = 0.25) #<- se puede cambiar el radio
vp.ring(pos=vp.vector(0,0,0),
             axis=vp.vector(0,0,1),
             radius=25, thickness=0.1) #<- debe cambiar el radio si cambia el radio arriba este es el exterior
vp.ring(pos=vp.vector(0,0,0),
             axis=vp.vector(0,0,1),
             radius=15, thickness=0.1) #<- debe cambiar el radio si cambia el radio arriba este es el interior

particula.vel = v 
#particula.pos_0 = p_0 <- checar notas de pelota_caja_circular
particula.momento = momento_0
camino = vp.curve(color = vp.vector(1,0,0))

t = 0
dt = 0.01 #<- se puede cambiar el paso temporal
radio_ext = 25 #<- se puede cambiar condicion exterior de la caja
radio_int = 15  #<- se puede cambiar condicion interior de la caja

while t<1:
    vp.rate(250)
    ##debo calcula rla fuerza, luego cambiar el momento,
    ##luego cambiar la posición.

    #calculo de fuerza:
    F_particula_peso = masa*campo_grav
    #cambiamos el momento:
    particula.momento = particula.momento + dt*F_particula_peso
    #cambiamos la posición:
    particula.pos = particula.pos + (dt/masa)*particula.momento
    #debo actualizar la velocidad:
    particula.vel = (1/masa)*particula.momento
    ##fin de la fuerza
    ##debo tomar los rebotes, por lo que basta aplicar las funciones rebote:
    rebote_ext(particula, radio_ext, dt)
    rebote_int(particula, radio_int, dt)
    particula.pos = particula.pos + dt*particula.vel
    camino.append(pos = particula.pos)