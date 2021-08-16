from math import pi
import pygame 
# Simulation Parameters
# big screen
# SCREEN_WIDTH = 1600 
# SCREEN_HEIGHT = 920 
# Small screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
PIX2M = 0.01  # factor to convert from pixels to meters
M2PIX = 100.0  # factor to convert from meters to pixels
RAD2DEGREE = 180/pi
N_PLAYERS = 500
N_SENSORS = 10
# Sample Time Parameters
FREQUENCY = 30.0  # simulation frequency
SAMPLE_TIME = 1.0 / FREQUENCY  # simulation sample time

# colors
COLOR_WHITE = (255,255,255)
COLOR_GRAY = (70, 66, 47)
COLOR_BLACK = (0, 0, 0)
COLOR_TRACK = (110, 110, 110)
COLOR_SENSOR = (0, 132, 180)
COLOR_RED = (248, 1, 3)
COLOR_YELLOW = (255, 255, 0)

MAP_PARAMETERS = [1, (0,0), False, ""]


# cars dimensions
CARS_WIDTH = 13
CARS_HEIGHT = 25
# sensor dimension
SENSOR_HEIGHT = CARS_HEIGHT - 10

# Move Parameters
FORWARD_SPEED = 0.2
BACKWARD_SPEED = -0.2
ANGULAR_SPEED = 0.1

# player limits
MAX_LINEAR_SPEED = 2.0
MAX_ANGULAR_SPEED = 60.0

# Finish line
# small screen
FINISH_LINE = ((906,506), (976, 506))
INIT_LINE = (910,435)
INIT_MULTIPLICATION = 65
COST_START = 2750
INITIAL_DISTANCE = 2627
# big screen
# INIT_MULTIPLICATION = 100
# INIT_LINE = (1436,635)
# FINISH_LINE = ((1435,714), (1559, 714))
# COST_START = 4210
# INITIAL_DISTANCE = 4150

# Pressing array
KEY_A = 97
KEY_D = 100
KEY_S = 115
KEY_W = 119
KEY_UP = 273
KEY_DOWN = 274
KEY_LEFT = 276
KEY_RIGHT = 275
KEYS = {
    "z": pygame.K_z,
    "x": pygame.K_x,
    "d": pygame.K_d,
    "a": pygame.K_a,
    "w": pygame.K_w,
    "s": pygame.K_s,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT 
}


# Neural network
NEURAL_PARAMS = [[N_SENSORS+2, 4 ,"sigmoid"],[4,4,"sigmoid"]]
ELITISM = 20
SIGMA = 0.5

POSE = (9.64, 4.3500000000000005)