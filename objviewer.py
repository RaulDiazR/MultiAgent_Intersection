import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Se carga el archivo de la clase Cubo
import sys
sys.path.append('..')
from CarO import CarO

import math

screen_width = 500
screen_height = 500
#vc para el obser.
FOVY=60.0
ZNEAR=1
ZFAR=3000
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X=0.0
EYE_Y=200.0
EYE_Z=0.01
CENTER_X=0
CENTER_Y=0
CENTER_Z=0
UP_X=0
UP_Y=1
UP_Z=0
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500

#Arreglo para el manejo de texturas

#Dimension del plano
DimBoard = 110

# Variables para el control del observador
theta = 0.0
radius = 300

pygame.init()

#cubo = Cubo(DimBoard, 1.0)
carros = []
ncarros = 1
        
matrix = [
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3],
    [1,1,1,1,1,1,5,3,1,2,2,2,2,1,5,3,1,1,1,1,1,1],
    [6,6,6,6,6,6,7,3,1,2,2,2,2,1,5,8,6,6,6,6,6,6],
    [4,4,4,4,4,4,7,3,1,2,2,2,2,1,5,8,4,4,4,4,4,4],
    [1,1,1,1,1,1,5,3,1,2,2,2,2,1,5,3,1,1,1,1,1,1],
    [2,2,2,2,2,1,5,3,1,2,2,2,2,1,5,3,1,2,2,2,2,2],
    [2,2,2,2,2,1,5,3,1,2,2,2,2,1,5,3,1,2,2,2,2,2],
    [2,2,2,2,2,1,5,3,1,2,2,2,2,1,5,3,1,2,2,2,2,2],
    [2,2,2,2,2,1,5,3,1,2,2,2,2,1,5,3,1,2,2,2,2,2],
    [1,1,1,1,1,1,5,3,1,1,1,1,1,1,5,3,1,1,1,1,1,1],
    [6,6,6,6,6,6,9,9,6,6,6,6,6,6,9,9,6,6,6,6,6,6],
    [4,4,4,4,4,4,9,9,4,4,4,4,4,4,9,9,4,4,4,4,4,4],
    [1,1,1,1,1,1,5,3,1,1,1,1,1,1,5,3,1,1,1,1,1,1],
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3]
    ]

def lookAt():
    glLoadIdentity()
    rad = theta * math.pi / 180
    newX = EYE_X * math.cos(rad) + EYE_Z * math.sin(rad)
    newZ = -EYE_X * math.sin(rad) + EYE_Z * math.cos(rad)
    gluLookAt(newX,EYE_Y,newZ,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    

 
def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    
    for i in range(ncarros):
        carros.append(CarO(DimBoard, 1))

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #Se dibujan los carros
    for obj in carros:
        obj.draw()
        obj.update(obj.Position[0], obj.Position[2], matrix)
        
    #Se dibuja el plano gris
    glColor3f(0, 0, 0)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0.1, 50)
    glVertex3d(DimBoard, 0.1, 50)
    glVertex3d(DimBoard, 0.1, 30)
    glVertex3d(-DimBoard, 0.1, 30)
    glEnd()

    glColor3f(0, 0, 0)
    glBegin(GL_QUADS)
    glVertex3d(-50, 0.1, -DimBoard)
    glVertex3d(-50, 0.1, DimBoard)
    glVertex3d(-30, 0.1, DimBoard)
    glVertex3d(-30, 0.1, -DimBoard)
    glEnd()

    glColor3f(0, 0, 0)
    glBegin(GL_QUADS)
    glVertex3d(50, 0.1, -DimBoard)
    glVertex3d(50, 0.1, DimBoard)
    glVertex3d(30, 0.1, DimBoard)
    glVertex3d(30, 0.1, -DimBoard)
    glEnd()

    glColor3f(0, 0, 0)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0.1, -50)
    glVertex3d(-30, 0.1, -50)
    glVertex3d(-30, 0.1, -30)
    glVertex3d(-DimBoard, 0.1, -30)
    glEnd()

    glColor3f(0, 0, 0)
    glBegin(GL_QUADS)
    glVertex3d(30, 0.1, -50)
    glVertex3d(DimBoard, 0.1, -50)
    glVertex3d(DimBoard, 0.1, -30)
    glVertex3d(30, 0.1, -30)
    glEnd()

    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()

    

    



    
    

    

done = False
Init()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    keys = pygame.key.get_pressed()  # Checking pressed keys
    if keys[pygame.K_RIGHT]:
        if theta > 359.0:
            theta = 0
        else:
            theta += 1.0
        lookAt()
    if keys[pygame.K_LEFT]:
        if theta < 1.0:
            theta = 360.0
        else:
            theta -= 1.0
        lookAt()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
        if event.type == pygame.QUIT:
            done = True
    display()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()