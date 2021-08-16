import pygame
from pygame.image import load
from pygame.rect import Rect
from pygame.gfxdraw import pie
from params import *
from utils import *
from Simulation.Scenario import Scenario
import numpy as np
from Simulation.main_neural import main_neural, load_neural
import matplotlib.pyplot as plt
import os


class Simulation(object):
    """
    Represents the simulation.
    """
    def __init__(self, player):
        """
        Creates the simulation.

        :param roomba: the roomba robot used in this simulation.
        :type roomba: Roomba
        """
        self.point_list = []
        self.players = player
        self.number_players = len(player)
        self.collision_array = None
        self.scenario = None
        self.simulationTime = 0
        self.generation = 1
        self.better_distance = 0
        self.betterPlayer = 0
        self.distancePlayers = np.zeros(self.number_players, dtype=float)


    def resetTime(self):
        
        self.simulationTime = 0


    def initScenario(self, window, mapParameters, cars):

        self.scenario = Scenario(self, window, mapParameters, cars, True)
        self.scenario.drawBackgroundImage()
        PATH = "arrays/"
        list_csv = os.listdir(PATH)
        csvs = [file for file in list_csv if '.csv' in file]
        if len(csvs) == 2:
            collision_array = np.loadtxt('arrays/collision_array.csv', dtype=int, delimiter=',')
            cost_array = np.loadtxt('arrays/cost_array.csv', dtype=int, delimiter=',')
            self.scenario.cost_array = cost_array
            self.scenario.collision_array = collision_array
            self.resetTime()
            self.scenario.initial = False
        else:
            collision_array = self.scenario.matrixCollision()
        self.set_collisionArray(collision_array)
        # plt.matshow(collision_array.transpose())
        # plt.show()

    
    def set_collisionArray(self, collision_array):

        self.collision_array = collision_array
        for player in self.players:
            player.set_collision_array(collision_array)

    def checkcollision(self):
        """
        Checks collision between the robot and the walls.

        :return: the bumper state (if a collision has been detected).
        :rtype: bool
        """
        for i in range(N_PLAYERS):
            x0 = M2PIX * self.players[i].pose.position.x
            y0 = M2PIX * self.players[i].pose.position.y
            
            if self.is_index_valid(round(x0), round(y0)):
                if self.scenario.cost_array[round(x0), round(y0)] < 0:
                    distance = self.distancePlayers[i]
                    self.players[i].distance = distance
                else:
                    distance = PIX2M * (INITIAL_DISTANCE -  self.scenario.cost_array[round(x0), round(y0)])
                    self.players[i].distance = distance
            else:
                distance = self.distancePlayers[i]
                self.players[i].distance = distance
            x1 = M2PIX * self.players[self.betterPlayer].pose.position.x
            y1 = M2PIX * self.players[self.betterPlayer].pose.position.y
            betterDistance = PIX2M * (INITIAL_DISTANCE -  self.scenario.cost_array[round(x1), round(y1)])
            if distance > betterDistance:
                self.betterPlayer = i

            self.distancePlayers[i] = distance
            
            
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    if self.is_index_valid(round(x0) + di, round(y0) + dj):
                        if self.collision_array[round(x0) + di, round(y0) + dj] == -1:
                            self.players[i].set_bumper_state(True)
            
            

            if 26.27 >= distance > self.better_distance:
                self.better_distance =  PIX2M * (INITIAL_DISTANCE -  self.scenario.cost_array[round(x0), round(y0)])

    def load_saved_neural(self, file_name):
        shapes_w = [a.shape for a in self.players[0].neural_network.weights]
        shapes_b = [a.shape for a in self.players[0].neural_network.bias]
        genes_w, genes_b = load_neural(file_name, shapes_w, shapes_b)
        i = 0
        for player in self.players:

            player.neural_network.weights = genes_w[i]
            player.neural_network.bias = genes_b[i]
            
            i = (i+1)%10

    def burntCarTime(self):
 
        for i in range(self.number_players):
            x0 = M2PIX * self.players[i].pose.position.x
            y0 = M2PIX * self.players[i].pose.position.y
            if self.is_index_valid(round(x0), round(y0)):
                cost = self.scenario.cost_array[round(x0), round(y0)]
            else:
                cost = 0
            cost_limit = COST_START - self.simulationTime * 5
            self.scenario.cust_limit = cost_limit

            if cost_limit <= cost:
                self.players[i].set_bumper_state(True)


        

    def restart_game(self):
        """
        Put a player on initial position.
        """
        restart = True
        for i in range(self.number_players):
            # x0 = M2PIX * self.players[i].pose.position.x
            # y0 = M2PIX * self.players[i].pose.position.y
            # if i == 10:
            #     print(x0, y0)
            # self.players[i].distance = INITIAL_DISTANCE -  self.scenario.cost_array[round(x0), round(y0)]
            if self.players[i].get_bumper_state() == False:
                restart = False

        if restart == True:
            players = self.players
            players = sorted(players, key=lambda player: player.distance, reverse=True) 
            distances = []
            for i in range(self.number_players):
                distances.append(players[i].distance)
            # print(distances)
            self.players = main_neural(self.players)

            for player in self.players:
                rand = np.random.randint(0, self.number_players)
                player.pose = Pose(PIX2M * round(INIT_LINE[0] + rand*INIT_MULTIPLICATION/self.number_players), PIX2M * INIT_LINE[1], -pi/2)
                # player.set_pose(Pose(POSE[0],POSE[1], -pi/2))
                player.set_bumper_state(False)
                player.distance = 0
                for j in range(N_SENSORS):
                    player.sensors[j].update(player.pose)

            self.generation += 1
            self.resetTime()


    def is_index_valid(self, i, j):
        return 0 <= i < SCREEN_WIDTH and 0 <= j < SCREEN_HEIGHT

    def update(self):
        """
        Updates the simulation.
        """
        for player in self.players:
            player.update()

        self.checkcollision()
        # laser
        self.burntCarTime()
        # restart game
        self.restart_game()
        
        self.simulationTime += 1
        
        

    def draw(self):
        """
        Draws the roomba and its movement history.

        :param window: pygame's window where the drawing will occur.
        """
        self.scenario.drawBackgroundImage()
        

    

def draw(simulation):
    """
    Redraws the pygame's window.

    :param simulation: the simulation object.
    :param window: pygame's window where the drawing will occur.
    """
    
    # print(simulation.player[0].pose.rotation)
    simulation.draw()
    pygame.display.update()



