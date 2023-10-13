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

screen_width = 500
screen_height = 500
#vc para el obser.
FOVY=60.0
ZNEAR=1
ZFAR=3000
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X=0.0
EYE_Y=50 #200
EYE_Z=200 #0.01
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

# Arreglo para el manejo de texturas
textures = []
filenames = ["pasto.bmp", "agua.bmp", "white.bmp", "atardecer.bmp", "atardecer_down.bmp"]

buildObj = OBJ("./Objetos3D/Building/Rv_Building_3.obj", swapyz=True)
buildObj.generate()

houseObj = OBJ("./Objetos3D/Bambo_House/Bambo_House/Bambo_House_obj/Bambo_House.obj", swapyz=True)
houseObj.generate()

treeObj = OBJ("./Objetos3D/low_poly_tree/Lowpoly_tree_sample.obj", swapyz=True)
treeObj.generate()

trafficObj = OBJ("./Objetos3D/traffic_light/semaforoEduardo1.obj", swapyz=False)
trafficObj.generate()

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

def Texturas(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image, "RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)

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

    for i in filenames:
        Texturas(i)
    
    for i in range(ncarros):
        carros.append(CarO(DimBoard, 1))

def drawSkybox():
    glEnable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)
    glColor3f(1.0, 1.0, 1.0)

    #Caras laterales
    glBindTexture(GL_TEXTURE_2D, textures[3])
    glBegin(GL_QUADS)

    #Cara Z negativo
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-250, 250, -250)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(250, 250, -250)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(250, -250, -250)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-250, -250, -250)

    #Cara X positivo
    glTexCoord2f(0.0, 0.0)
    glVertex3d(250, 250, -250)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(250, 250, 250)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(250, -250, 250)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(250, -250, -250)

    #Cara Z Positivo
    glTexCoord2f(0.0, 0.0)
    glVertex3d(250, 250, 250)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-250, 250, 250)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-250, -250, 250)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(250, -250, 250)

    #Cara X Negativa
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-250, 250, 250)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-250, 250, -250)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-250, -250, -250)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-250, -250, 250)

    glEnd()

    #Cara inferior
    glBindTexture(GL_TEXTURE_2D, textures[4])
    glBegin(GL_QUADS)

    glTexCoord2f(0.0, 0.0)
    glVertex3d(-250, -250, -250)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(250, -250, -250)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(250, -250, 250)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-250, -250, 250)

    glEnd()
    glBindTexture(GL_TEXTURE_2D, textures[2])
    glEnable(GL_DEPTH_TEST)

def drawBuilding(x, z, tz, tx, sx, sz, sy, obj):
    glPushMatrix()
    glTranslate(x, 0.1, z)
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glRotate(270,1,0,0)
    glRotate(tz,0,0,1)
    glRotate(tx,1,0,0)
    scaleVal = 1
    glScalef(1*sx, 1*sz, 1*sy)
    obj.render()
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)
    glPopMatrix()

def drawGrass():
    glPushMatrix()
    #glScaled(3, 3, 3)
    glColor3f(1.0, 1.0, 1.0)
        
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[0])
        
    glBegin(GL_QUADS)
        
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-DimBoard, 0.1, 20)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-60, 0.1, 20)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-60, 0.1, -20)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-DimBoard, 0.1, -20)

    glTexCoord2f(0.0, 0.0)
    glVertex3d(60, 0.1, 20)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(DimBoard, 0.1, 20)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(DimBoard, 0.1, -20)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(60, 0.1, -20)

    glEnd()
    glDisable(GL_TEXTURE_2D)
            
    glPopMatrix()

def drawWater():
    glPushMatrix()
    #glScaled(3, 3, 3)
    glColor3f(1.0, 1.0, 1.0)
        
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[1])
        
    glBegin(GL_QUADS)
        
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-DimBoard, 0.1, -60)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-60, 0.1, -60)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-60, 0.1, -DimBoard)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-DimBoard, 0.1, -DimBoard)

    glTexCoord2f(0.0, 0.0)
    glVertex3d(60, 0.1, -60)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(DimBoard, 0.1, -60)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(DimBoard, 0.1, -DimBoard)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(60, 0.1, -DimBoard)

    glTexCoord2f(0.0, 0.0)
    glVertex3d(-DimBoard, 0.1, DimBoard)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-60, 0.1, DimBoard)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-60, 0.1, 60)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-DimBoard, 0.1, 60)

    glTexCoord2f(0.0, 0.0)
    glVertex3d(60, 0.1, DimBoard)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(DimBoard, 0.1, DimBoard)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(DimBoard, 0.1, 60)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(60, 0.1, 60)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, textures[2])
    glDisable(GL_TEXTURE_2D)
            
    glPopMatrix()

def drawTrees():
    #Arboles de la derecha
    drawBuilding(-65, -15, 0, 0, 0.5, 0.5, 0.5, treeObj)
    drawBuilding(-70, 5, 110, 0, 0.5, 0.5, 0.5, treeObj)
    drawBuilding(-100, -15, 40, 0, 0.5, 0.5, 0.5, treeObj)
    drawBuilding(-95, 15, 75, 0, 0.5, 0.5, 0.5, treeObj)
    drawBuilding(-90, -3, 90, 0, 0.5, 0.5, 0.5, treeObj)

    #Arboles de la Izquierda
    drawBuilding(70, -10, 0, 0, 0.5, 0.5, 0.5, treeObj)
    drawBuilding(80, 10, 90, 0, 0.5, 0.5, 0.5, treeObj)
    drawBuilding(90, -10, 20, 0, 0.5, 0.5, 0.5, treeObj)
    drawBuilding(100, 10, 160, 0, 0.5, 0.5, 0.5, treeObj)
    drawBuilding(65, 5, 100, 0, 0.5, 0.5, 0.5, treeObj)

def drawTraffic():

    #Interseccion 1
    drawBuilding(25, -25, 90, 90, 2, 2, 2, trafficObj)
    drawBuilding(55, -25, 180, 90, 2, 2, 2, trafficObj)
    drawBuilding(25, -55, 0, 90, 2, 2, 2, trafficObj)
    drawBuilding(55, -55, 270, 90, 2, 2, 2, trafficObj)

    #Interseccion 2
    drawBuilding(-55, -55, 0, 90, 2, 2, 2, trafficObj)
    drawBuilding(-25, -55, 270, 90, 2, 2, 2, trafficObj)
    drawBuilding(-55, -25, 90, 90, 2, 2, 2, trafficObj)
    drawBuilding(-25, -25, 180, 90, 2, 2, 2, trafficObj)

    #Debajo Interseccion 1
    drawBuilding(55, 25, 0, 90, 2, 2, 2, trafficObj)
    drawBuilding(55, 55, 270, 90, 2, 2, 2, trafficObj)

    #Debajo Interseccion 2
    drawBuilding(-55, 25, 90, 90, 2, 2, 2, trafficObj)
    drawBuilding(-55, 55, 180, 90, 2, 2, 2, trafficObj)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    #Se dibuja el Skybox
    drawSkybox()

    #Se dibujan los carros
    for obj in carros:
        obj.draw()
        obj.update(obj.Position[0], obj.Position[2], matrix)

    #Se dibujan el pasto
    drawGrass()

    #Se dibuja el agua
    drawWater()

    #Se dibujan buildings
    drawBuilding(0, 40, 90, 0, 3.3, 2, 2, buildObj)
    drawBuilding(0, -80, 270, 0, 1.3, 2, 3, buildObj)

    #Se dibujan arboles
    drawTrees()

    #Se dibujan los semaforos
    drawTraffic()

    #Se dibuja el plano gris y las calles
    glColor3f(0, 0, 0)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0.1, -50)
    glVertex3d(DimBoard, 0.1, -50)
    glVertex3d(DimBoard, 0.1, -30)
    glVertex3d(-DimBoard, 0.1, -30)
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
    glVertex3d(-DimBoard, 0.1, 50)
    glVertex3d(-30, 0.1, 50)
    glVertex3d(-30, 0.1, 30)
    glVertex3d(-DimBoard, 0.1, 30)
    glEnd()

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
    pygame.time.wait(10)

pygame.quit()