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
N_SENSORS = 11

# Sample Time Parameters
FREQUENCY = 50.0  # simulation frequency
SAMPLE_TIME = 1.0 / FREQUENCY  # simulation sample time

# colors
COLOR_WHITE = (255,255,255)
COLOR_GRAY = (70, 66, 47)
COLOR_BLACK = (0, 0, 0)
COLOR_TRACK = (110, 110, 110)
COLOR_SENSOR = (0, 132, 180)
COLOR_RED = (248, 1, 3)
COLOR_YELLOW = (255, 255, 0)

MAP_PARAMETERS = [1, (0,0)]


# cars dimensions
CARS_WIDTH = 14
CARS_HEIGHT = 30
# sensor dimension
SENSOR_HEIGHT = CARS_HEIGHT - 10

# Move Parameters
FORWARD_SPEED = 2.0
BACKWARD_SPEED = -1.0
ANGULAR_SPEED = 2.0

# player limits
MAX_LINEAR_SPEED = 3 * FORWARD_SPEED
MAX_ANGULAR_SPEED = 3 * ANGULAR_SPEED

# Finish line
FINISH_LINE = ((906,506), (976, 506))

# cost start
COST_START = 2750
INITIAL_DISTANCE = 2627

# Pressing array
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
NEURAL_SIZE = [N_SENSORS + 2, 4, 4]
ELITISM_RATE = 0.04