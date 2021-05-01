import pygame
from params import *

cdef Keyboard(int key, (int, (int, int)) mapParameters, 
                            object carsParameters, object pressingArray):


    cdef (int, int) pos = mapParameters[1]

    if key == KEY["z"]:
        mapParameters[0] = 2
    elif key == KEY["x"]:
        mapParameters[0] = 1
        mapParameters[1] = (0,0)

    if (key == KEY["d"] or pressingArray[KEY["d"]]) and mapParameters[0] == 2 :
        mapParameters[1] = limitPosition(pos, (-100, 0))
    elif (key == KEY["a"] or pressingArray[KEY["a"]]) and mapParameters[0] == 2:
        mapParameters[1] = limitPosition(pos, (100, 0))

    if (key == KEY["w"] or pressingArray[KEY["w"]]) and mapParameters[0] == 2:
        mapParameters[1] = limitPosition(pos, (0, 100))
    elif (key == KEY["s"] or pressingArray[KEY["s"]]) and mapParameters[0] == 2:
        mapParameters[1] = limitPosition(pos, (0, -100))

    if key == KEY["up"] or pressingArray[KEY["up"]]:
        carsParameters.append("up")
    elif key == KEY["down"] or pressingArray[KEY["down"]]:
        carsParameters.append("down")

    if key == KEY["left"]  or pressingArray[KEY["left"]]:
        carsParameters.append("left")
    elif key == KEY["right"]  or pressingArray[KEY["right"]]:
        carsParameters.append("right")


    
    return mapParameters, carsParameters


cpdef (int, int) limitPosition((int, int) pos, (int, int) increse):
    cdef int x, y
    if pos[0] + increse[0] < -SCREEN_WIDTH:
        x = -SCREEN_WIDTH
    elif pos[0] + increse[0] > 0:
        x = 0
    else:
        x = pos[0] + increse[0]

    if pos[1] + increse[1] < -SCREEN_HEIGHT:
        y = -SCREEN_HEIGHT
    elif pos[1] + increse[1] > 0:
        y = 0
    else:
        y = pos[1] + increse[1]
    return (x,y)
    