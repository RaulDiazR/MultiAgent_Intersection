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
from objloader import *
import math

import requests
import json

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


URL_BASE = "http://localhost:5000"
r = requests.post(URL_BASE+ "/games", allow_redirects=False)
LOCATION = r.headers["Location"]

carsMesa = json.loads(r.headers["cars"])

#Dimension del plano
DimBoard = 110

# Variables para el control del observador
theta = 0.0
radius = 300

buildObj = OBJ("./Objetos3D/Building/Rv_Building_3.obj", swapyz=True)
buildObj.generate()

#houseObj = OBJ("./Objetos3D/House/house.obj", swapyz=True)
#houseObj.generate()

pygame.init()



#cubo = Cubo(DimBoard, 1.0)
carros = []
ncarros = len(carsMesa)

carrosCords = []

# Se guardan las posiciones iniciales de los robots
for car in carsMesa:
    x, z = car['x']*10 - DimBoard, car['z']*10 - DimBoard
    carDir = (car['speedX'], car['speedZ'])
    carrosCords.append(((x,z), carDir))
    
        
matrix = [
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3],
    [1,1,1,1,1,1,5,7,1,1,1,1,1,1,5,7,1,1,1,1,1,1],
    [6,6,6,6,6,6,8,10,6,6,6,6,6,6,8,10,6,6,6,6,6,6],
    [4,4,4,4,4,4,9,11,4,4,4,4,4,4,9,11,4,4,4,4,4,4],
    [1,1,1,1,1,1,5,7,1,2,2,2,2,1,5,7,1,1,1,1,1,1],
    [2,2,2,2,2,1,5,7,1,2,2,2,2,1,5,7,1,2,2,2,2,2],
    [2,2,2,2,2,1,5,7,1,2,2,2,2,1,5,7,1,2,2,2,2,2],
    [2,2,2,2,2,1,5,7,1,2,2,2,2,1,5,7,1,2,2,2,2,2],
    [2,2,2,2,2,1,5,7,1,2,2,2,2,1,5,7,1,2,2,2,2,2],
    [1,1,1,1,1,1,5,7,1,2,2,2,2,1,5,7,1,1,1,1,1,1],
    [6,6,6,6,6,6,8,7,1,2,2,2,2,1,5,7,6,6,6,6,6,6],
    [4,4,4,4,4,4,9,7,1,2,2,2,2,1,5,11,4,4,4,4,4,4],
    [1,1,1,1,1,1,5,7,1,2,2,2,2,1,5,7,1,1,1,1,1,1],
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3]
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
        carros.append(CarO(DimBoard, 1, carrosCords[i][0], carrosCords[i][1]))

def drawBuilding(x, z, obj):
    glPushMatrix()
    glTranslate(x, 0.1, z)
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glRotate(270,1,0,0)
    scaleVal = 2
    glScalef(scaleVal,scaleVal,scaleVal)
    obj.render()
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)
    glPopMatrix()

def display():
    r = requests.get(URL_BASE+LOCATION)
    carsMesa = json.loads(r.headers["cars"])
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #Se dibujan los carros
    for i in range(len(carros)):
        carros[i].draw()
        carDir = (carsMesa[i]['speedX'], carsMesa[i]['speedZ'])
        carros[i].update(carsMesa[i]['x']*10 - DimBoard, carsMesa[i]['z']*10 - DimBoard, carDir, matrix)

    #building 1 test
    drawBuilding(-90, 0, buildObj)
    drawBuilding(90, 0, buildObj)
        
    #Se dibuja el plano gris
    
    # Calle horizontal completa superior
    glColor3f(0, 0, 0)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0.1, -50)
    glVertex3d(DimBoard, 0.1, -50)
    glVertex3d(DimBoard, 0.1, -30)
    glVertex3d(-DimBoard, 0.1, -30)
    glEnd()

    # Calle vertical completa derecha
    glColor3f(0, 0, 0)
    glBegin(GL_QUADS)
    glVertex3d(-50, 0.1, -DimBoard)
    glVertex3d(-50, 0.1, DimBoard)
    glVertex3d(-30, 0.1, DimBoard)
    glVertex3d(-30, 0.1, -DimBoard)
    glEnd()

    # Calle vertical completa derecha
    glColor3f(0, 0, 0)
    glBegin(GL_QUADS)
    glVertex3d(50, 0.1, -DimBoard)
    glVertex3d(50, 0.1, DimBoard)
    glVertex3d(30, 0.1, DimBoard)
    glVertex3d(30, 0.1, -DimBoard)
    glEnd()
    
    # Calle horizontal parcial izquierda
    glColor3f(0, 0, 0)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0.1, 50)
    glVertex3d(-30, 0.1, 50)
    glVertex3d(-30, 0.1, 30)
    glVertex3d(-DimBoard, 0.1, 30)
    glEnd()

    # Calle horizontal parcial derecha
    glColor3f(0, 0, 0)
    glBegin(GL_QUADS)
    glVertex3d(30, 0.1, 50)
    glVertex3d(DimBoard, 0.1, 50)
    glVertex3d(DimBoard, 0.1, 30)
    glVertex3d(30, 0.1, 30)
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
    pygame.time.wait(0)

pygame.quit()