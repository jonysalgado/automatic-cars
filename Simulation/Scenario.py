import pygame
from pygame.rect import Rect
from pygame.gfxdraw import pie
from math import pi, sqrt
import numpy as np
from params import *
# remove after
import matplotlib.pyplot as plt
import time
import pandas as pd


class Scenario(object):
    def __init__(self, simulation, window, mapParameters, cars, initial):
        self.simulation = simulation
        self.window = window
        self.mapParameters = mapParameters
        self.cars = cars
        self.collision_array = None
        self.initial = initial
        self.cost_array = None
        self.n_players = simulation.number_players
        self.get_images()
        self.time = time.time()
        self.cust_limit = 1000000

    def get_images(self):
        self.burntCar = []
        for i in range(self.n_players):
            self.burntCar.append(pygame.image.load("./Img/carroQueimado.png"))
            self.burntCar[i] = pygame.transform.scale(self.burntCar[i], (CARS_HEIGHT, CARS_WIDTH))
        self.explosion = []
        for j in range(1, 45):
            self.explosion.append(pygame.image.load("./Img/explosion/exp (" + str(j) + ").png"))
            self.explosion[j-1] = pygame.transform.scale(self.explosion[j-1], (200, 200))
        
        self.fundo = pygame.image.load('./Img/star.png')
        self.fundo = pygame.transform.scale(self.fundo, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.pista = pygame.image.load('./Img/pista.png')
        self.pista = pygame.transform.scale(self.pista, (SCREEN_WIDTH -200, SCREEN_HEIGHT))

        

    def  drawBackgroundImage(self):   

        sensorPoint = pygame.image.load("./Img/luzAzul.png")
        # neural_point = pygame.image.load("./Img/luz.png")
        # neural_point = pygame.transform.scale(neural_point, (SENSOR_HEIGHT+100, SENSOR_HEIGHT+100)) 
        sensorPoint = pygame.transform.scale(sensorPoint, (SENSOR_HEIGHT, SENSOR_HEIGHT))  
        
        if self.initial == False:
            self.window.blit(self.fundo, (0,0))
        self.window.blit(self.pista, (200,0))


        # cars
        for i in range(self.n_players):
            self.cars[i] = pygame.transform.scale(self.cars[i], (CARS_HEIGHT, CARS_WIDTH))
            car_rotate = pygame.transform.rotate(self.cars[i], round(-self.simulation.players[i].pose.rotation * RAD2DEGREE)%360)
            x = M2PIX * self.simulation.players[i].pose.position.x
            y = M2PIX * self.simulation.players[i].pose.position.y
            if self.simulation.players[i].bumper_state:
                car_rotate = pygame.transform.rotate(self.burntCar[i], round(-self.simulation.players[i].pose.rotation * RAD2DEGREE)%360)
                self.window.blit(car_rotate, (x-car_rotate.get_rect().center[0], y-car_rotate.get_rect().center[1]))
            else:
                if self.initial == False:
                        # if i == 0:
                        #     self.drawSensors(self.simulation.players[i].sensors, (x,y))
                    self.window.blit(car_rotate, (x-car_rotate.get_rect().center[0], y-car_rotate.get_rect().center[1]))
        # print(time.time() - start)
        if time.time() - self.time > 3:
            best = self.simulation.betterPlayer
            self.drawSensors(self.simulation.players[best].sensors, self.simulation.players[best].pose.position, sensorPoint)
            self.drawLaser()
        self.drawScore()
        windowScale = pygame.transform.scale(pygame.display.get_surface(), (SCREEN_WIDTH * self.mapParameters[0], SCREEN_HEIGHT * self.mapParameters[0]))
        self.window.fill((0,0,0))
        self.window.blit(windowScale, self.mapParameters[1])
        # self.window.blit(neural_point, (SENSOR_HEIGHT, SENSOR_HEIGHT))


    def drawSensors(self, sensors, centerPos, sensorPoint):
        # print(sensors[0].distance()['a']['a'], sensors[0].distance()['a']['b'], sensors[0].distance()["b"])
        for i in range(N_SENSORS):
            pygame.draw.line(self.window, COLOR_SENSOR, 
                                    (sensors[i].distance()['a']['a'], sensors[i].distance()['a']['b']), 
                                    (M2PIX * centerPos.x, M2PIX * centerPos.y), 1)
            self.window.blit(sensorPoint, (sensors[i].distance()['a']['a'] - SENSOR_HEIGHT/2, sensors[i].distance()['a']['b'] - SENSOR_HEIGHT/2))

    def drawLaser(self):
        (x,y) = np.where(self.cost_array == self.cust_limit)
        # print(x)
        if len(x) != 0:
            cordinate = list(zip(x,y))
            cordinate = sorted(cordinate, key= lambda index: index[0])
            pygame.draw.line(self.window, COLOR_YELLOW, 
                                        (cordinate[0][0], cordinate[0][1]), 
                                        (cordinate[-1][0], cordinate[-1][1]), 3)
    def drawScore(self):
        
        font = pygame.font.SysFont('Comic Sans MS', 34)
        generation = "Gera????o: " + str(self.simulation.generation)
        textsurface = font.render(generation, False, (255, 255, 255))
        self.window.blit(textsurface, (20,300))
        distance = "Melhor dist??ncia: "
        textsurface = font.render(distance, False, (255, 255, 255))
        self.window.blit(textsurface, (15,340))
        distance = str(round(self.simulation.better_distance * M2PIX, 2)) + " pixels"
        textsurface = font.render(distance, False, (255, 255, 255))
        self.window.blit(textsurface, (20,365))

        if self.simulation.better_distance >= (INITIAL_DISTANCE - 2) * PIX2M:
            conclusion = "Eu aprendi a dirigir!"
            textsurface = font.render(conclusion, False, (255, 255, 255))
            self.window.blit(textsurface, (15,450))


    def matrixCollision(self):
        pxarray = pygame.PixelArray(self.window)
        array = np.array(pxarray, dtype="int32")
        # plt.matshow(array)
        # plt.show()
        for i in range(SCREEN_WIDTH):
            for j in range(SCREEN_HEIGHT):
                if array[i,j] == self.window.map_rgb((110,110,110)):
                    array[i, j] = 1
                # elif  array[i,j] >= self.window.map_rgb((118,118,118)):
                #     array[i, j] = 0
                else:
                    array[i,j] = -1
        self.collision_array = array
        # plt.matshow(array)
        # plt.show()
        self.cost_function()
        self.initial = False
        np.savetxt('arrays/collision_array.csv', array, fmt='%i', delimiter=',')
        np.savetxt('arrays/cost_array.csv', self.cost_array, fmt='%i', delimiter=',')
        
        return array

    def cost_function(self):
        array = np.copy(self.collision_array)
        nodeArray = np.empty((SCREEN_WIDTH, SCREEN_HEIGHT), dtype=Node)

        # preparing array
        for i in range(SCREEN_WIDTH):
            for j in range(SCREEN_HEIGHT):
                if array[i,j] == 1:
                    nodeArray[i, j] = Node(i,j,-2)
                else:
                    nodeArray[i, j] = Node(i,j,-1)

        # queue of pixels
        queue = []
        # set zero for finish line
        initialPoint = FINISH_LINE[0]
        finishPoint = FINISH_LINE[1]
        for i in range(initialPoint[0], finishPoint[0] + 1):
            nodeArray[i, initialPoint[1]].setCost(0)
            queue.append(nodeArray[i, initialPoint[1]])


        while len(queue) != 0:
            node = queue.pop(0)
            # print(type(node.neighbor))
            for nodes in node.neighbor:
                if nodeArray[nodes].cost == -2:
                    queue.append(nodeArray[nodes])
                    nodeArray[nodes].setCost(node.cost + 1)

        
        for i in range(SCREEN_WIDTH):
            for j in range(SCREEN_HEIGHT):
                array[i, j] = nodeArray[i,j].cost

        self.cost_array = array
        # plt.matshow(array)
        # plt.show()
        self.simulation.resetTime()

class Node(object):

    def __init__(self, i, j, cost):
        
        self.i = i
        self.j = j
        self.cost = cost
        self.neighbor = self.getNeighbor()

    def setCost(self, cost):
        
        self.cost = cost

    def getNeighbor(self):
        neighbor = []
        for di in range(-1,2):
            for dj in range(-1,2):
                if self.is_index_valid(self.i+di, self.j+dj) and (di != 0 or dj != 0):
                    neighbor.append((self.i+di, self.j+dj))
            
        return neighbor

    def is_index_valid(self, i, j):
        return 0 <= i < SCREEN_WIDTH and 0 <= j < SCREEN_HEIGHT