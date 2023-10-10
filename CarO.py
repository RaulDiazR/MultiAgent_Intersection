import pygame
#from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

from pygame.locals import *

#cargamos las bibliotecas de openGl


import random
import math
from objloader import *
viewport = (500,500)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 100, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.8, 0.8, 0.8, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded

# LOAD OBJECT AFTER PYGAME INIT
#obj = OBJ(sys.argv[1], swapyz=True)
obj = OBJ("./Objetos3D/Car-Model/Car.obj", swapyz=True)
obj.generate()

class CarO:
    
    def __init__(self, dim, vel, pos, dir):
        
        self.DimBoard = dim
        #Se inicializa una posicion aleatoria en el tablero
        print(pos)
        self.Position = [pos[0], 0.1, pos[1]]
        #self.Position[0]= random.randint(-dim, dim)
        #Inicializar las coordenadas (x,y,z) del cubo en el tablero
        #almacenandolas en el vector Position
        #...
        #Se inicializa un vector de direccion aleatorio
        self.Direction = [0, 0, -1]
        self.Direction[0] = dir[0]
        self.Direction[2] = dir[1]
        
        #El vector aleatorio debe de estar sobre el plano XZ (la altura en Y debe ser fija)
        #Se normaliza el vector de direccion
        #...
        #Se cambia la maginitud del vector direccion con la variable vel
        #...
        #self.Direction = [random.uniform(-1, 1), 0.0, random.uniform(-1, 1)]
        
        # Generar un vector aleatorio
        #random_direction = [random.uniform(-1, 1), 0.0, random.uniform(-1, 1)]

        # Normalizar el vector aleatorio
        magnitude = math.sqrt(self.Direction[0] ** 2 + self.Direction[2] ** 2)
        normalized_direction = [self.Direction[0] / magnitude, self.Direction[1] / magnitude, self.Direction[2] / magnitude]

        # Multiplicar por la velocidad deseada
        self.Direction = [normalized_direction[0] * vel, normalized_direction[1] * vel, normalized_direction[2] * vel]

        #Variable para revisar si entro en una nueva celda
        self.lastCell = 0


        

    def update(self, x, z, dir, matrix):

        # if self.Position[0] >= self.DimBoard:
        #     self.Position[0] -= 210
        #     x = self.Position[0]
        #     #self.Position[0] = self.DimBoard
        #     #self.Direction[0] *= -1
        # elif self.Position[0] <= -self.DimBoard:
        #     self.Position[0] += 210
        #     x = self.Position[0]
        #     #self.Position[0] = -self.DimBoard
        #     #self.Direction[0] *= -1
            
        # if self.Position[2] >= self.DimBoard:
        #     self.Position[2] -= 210
        #     z = self.Position[2]
        #     #self.Position[2] = self.DimBoard
        #     #self.Direction[2] *= -1
        # elif self.Position[2] <= -self.DimBoard:
        #     self.Position[2] += 210
        #     z = self.Position[2]
        #     #self.Position[2] = -self.DimBoard
        #     #self.Direction[2] *= -1
        # #print(self.Position[0])
        # #print(self.Position[2])

        # xm = int((math.floor(x) + 110) / 10)
        # zm = int((math.floor(z) + 110) / 10)

        # celda = matrix[zm][xm]

        # if (celda != self.lastCell):
        #     self.lastCell = celda
        #     if celda == 3:
        #         self.Direction[2] = 1
        #         self.Direction[0] = 0
        #     elif celda == 4:
        #         self.Direction[0] = 1
        #         self.Direction[2] = 0
        #     elif celda == 5:
        #         self.Direction[2] = -1
        #         self.Direction[0] = 0
        #     elif celda == 6:
        #         self.Direction[0] = -1
        #         self.Direction[2] = 0
        #     elif celda == 7:
        #         if self.Direction[0] == 1:
        #             self.Direction[0] = 0
        #             self.Direction[2] = -1
        #         else:
        #             if matrix[xm][zm - 1] == 6:
        #                 if random.randint(0,1) == 0:
        #                     self.Direction[2] = 0
        #                     self.Direction[0] = -1
        #     elif celda == 8:
        #         if self.Direction[0] == -1:
        #             self.Direction[0] = 0
        #             self.Direction[2] = 1
        #         else:
        #             if matrix[xm][zm + 1] == 4:
        #                 if random.randint(0,1) == 0:
        #                     self.Direction[2] = 0
        #                     self.Direction[0] = 1
        #     elif celda == 9:
        #         if self.Direction[2] == -1:
        #             if matrix[xm][zm - 1] == 6:
        #                 self.Direction[2] = 0
        #                 self.Direction[0]= -1
        #         elif self.Direction[2] == 1:
        #             if matrix[xm][zm + 1] == 4:
        #                 self.Direction[2] = 0
        #                 self.Direction[0] = 1
        #         elif self.Direction[0] == -1:
        #             if matrix[xm - 1][zm] == 3:
        #                 self.Direction[0] = 0
        #                 self.Direction[2] = 1
        #         elif self.Direction[0] == -1:
        #             if matrix[xm + 1][zm] == 5:
        #                 self.Direction[0] = 0
        #                 self.Direction[2] = -1

        
                    
        self.Position[0] = x
        self.Position[2] = z
        
        self.Direction[0] = dir[0]
        self.Direction[2] = dir[1]

    def draw(self):
        glPushMatrix()
        #glColor3f(1.0, 1.0, 1.0)
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        car_direction = [self.Direction[0], self.Direction[1], self.Direction[2]]
        magnitude = math.sqrt(car_direction[0] ** 2 + car_direction[2] ** 2)
        if magnitude > 0:
            car_direction[0] /= magnitude
            car_direction[2] /= magnitude
        else:
            car_direction = [0, 0, 1]

        # Calcular el ángulo de rotación para que la bandeja apunte en la dirección correcta
        angle = math.degrees(math.atan2(car_direction[0], car_direction[2]))

        glRotatef(angle, 0, 1, 0)  # Rotar el carro
        glRotatef(180, 0, 1, 0)  # Rotar el carro
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glRotate(270,1,0,0)
        scaleVal = 2
        glScalef(scaleVal,scaleVal,scaleVal)
        obj.render()
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glPopMatrix()

        

    
