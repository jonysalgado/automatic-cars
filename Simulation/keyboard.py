import pygame
from params import *

def Keyboard(key, mapParameters, carsParameters):
    pressingArray = pygame.key.get_pressed()
    # print(pressingArray[KEY_D])
    pos = mapParameters[1]
    if key == pygame.K_z:
        mapParameters[0] = 2
    elif key == pygame.K_x:
        mapParameters[0] = 1
        mapParameters[1] = (0,0)

    if key == pygame.K_F1:
        mapParameters[2] = True

    if (key == pygame.K_d or pressingArray[KEY_D]) and mapParameters[0] == 2 :
        mapParameters[1] = limitPosition(pos, (-100, 0))
    elif (key == pygame.K_a or pressingArray[KEY_A]) and mapParameters[0] == 2:
        mapParameters[1] = limitPosition(pos, (100, 0))

    if (key == pygame.K_w or pressingArray[KEY_W]) and mapParameters[0] == 2:
        mapParameters[1] = limitPosition(pos, (0, 100))
    elif (key == pygame.K_s or pressingArray[KEY_S]) and mapParameters[0] == 2:
        mapParameters[1] = limitPosition(pos, (0, -100))

    if key == pygame.K_UP or pressingArray[KEY_UP]:
        carsParameters.append("up")
    elif key == pygame.K_DOWN or pressingArray[KEY_DOWN]:
        carsParameters.append("down")

    if key == pygame.K_LEFT or pressingArray[KEY_LEFT]:
        carsParameters.append("left")
    elif key == pygame.K_RIGHT or pressingArray[KEY_RIGHT]:
        carsParameters.append("right")
    
    # print(pressingArray[KEY_UP])


    
    return mapParameters, carsParameters


def limitPosition(pos, increse):
    position = [pos[0], pos[1]] 
    if pos[0] + increse[0] < -SCREEN_WIDTH:
        position[0] = -SCREEN_WIDTH
    elif pos[0] + increse[0] > 0:
        position[0] = 0
    else:
        position[0] = pos[0] + increse[0]

    if pos[1] + increse[1] < -SCREEN_HEIGHT:
        position[1] = -SCREEN_HEIGHT
    elif pos[1] + increse[1] > 0:
        position[1] = 0
    else:
        position[1] = pos[1] + increse[1]
    return tuple(position)