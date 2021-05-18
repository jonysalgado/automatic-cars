from utils cimport *
from libc.math cimport sqrt, cos, abs, M_PI
from params import SCREEN_WIDTH, SCREEN_HEIGHT, M2PIX
import numpy as np
cimport numpy as np
cimport sensors


cdef struct tuple_double_double:
    double a
    double b

cdef struct tuple_tuple_double:
    tuple_double_double a
    double b

cdef class Sensors:

    def __cinit__(self, np.ndarray[int, ndim=2] collide_array,
                       center_player, int number):
        
        self.collide_array = collide_array
        self.centerPose = center_player
        self.number = number
        self.angle = 2*M_PI*number/12

    cdef inline double totalAngle(self):
        return self.angle + self.centerPose.rotation

    cdef inline double normalAngle(self, double angle):
        """
        Return a angle between 0 and 2*pi
        """

        while angle >= 2*M_PI:
            angle -= 2*M_PI
        
        while angle < 0:
            angle += 2*M_PI
        
        return angle
    
    cpdef tuple_tuple_double distance(self):
        
        cdef double centerX, centerY, totalAngle, distance
        cdef tuple_double_double point
        cdef tuple_tuple_double result

        centerY = self.centerPose.position.y * M2PIX
        centerX = self.centerPose.position.x * M2PIX
        totalAngle = self.totalAngle()

        if abs(self.normalAngle(totalAngle) - M_PI/2) < 1.0e-3:
            point = self.getFinalPosition(1)
            if point != None:
                distance = sqrt((point.a-centerX)**2 + (point.b-centerY)**2)
            else:
                distance = 0
                point.a, point.b = centerX, centerY
                result.a, result.b = point, distance
            return result
        
        elif abs(self.normalAngle(totalAngle) - 3*M_PI/2) < 1.0e-3:
            point = self.getFinalPosition(2)
            if point != None:
                distance = sqrt((point.a-centerX)**2 + (point.b-centerY)**2)
            else:
                distance = 0
                point.a, point.b = centerX, centerY
                result.a, result.b = point, distance
            return result

        elif cos(self.normalAngle(totalAngle)) > 0:
            point = self.getFinalPosition(3)
            if point != None:
                distance = sqrt((point.a-centerX)**2 + (point.b-centerY)**2)
            else:
                distance = 0
                point.a, point.b = centerX, centerY
                result.a, result.b = point, distance
            return result
        
        elif cos(self.normalAngle(totalAngle)) < 0:
            point = self.getFinalPosition(4)
            if point != None:
                distance = sqrt((point.a-centerX)**2 + (point.b-centerY)**2)
            else:
                distance = 0
                point.a, point.b = centerX, centerY
                result.a, result.b = point, distance
            return result

    cdef inline tuple_double_double getFinalPosition(self, int case):

        cdef double centerX, centerY, j
        cdef tuple_double_double point

        centerY = self.centerPose.position.y * M2PIX
        centerX = self.centerPose.position.x * M2PIX
        # angle is 90 degrees
        if case == 1:
            for i in range(round(centerY), SCREEN_HEIGHT):
                if self.is_index_valid(round(centerX), i):
                    if self.collide_array[round(centerX), i] == 0:
                        point.a, point.b = centerX, i
                        return point

        # angle is 270 degrees
        elif case == 2:
            for i in range(round(centerY), 0, -1):
                if self.is_index_valid(round(centerX), i):
                    if self.collide_array[round(centerX), i] == 0:
                        point.a, point.b = centerX, i
                        return point
            
        # angle is between 3*pi/2 and pi/2
        elif case == 3:
            function = function_linear(self.normalAngle(self.totalAngle()), self.centerPose)
            for i in range(round(centerX), SCREEN_WIDTH):
                j = function.y(i)
                if self.is_index_valid(i, round(j)):
                    if self.collide_array[i, round(j)] == 0:
                        point.a, point.b = i, j
                        return point

        # angle is between pi/2 and 3*pi/2
        elif case == 4:
            function = function_linear(self.normalAngle(self.totalAngle()), self.centerPose)
            for i in range(round(centerX), 0, -1):
                j = function.y(i)
                if self.is_index_valid(i, round(j)):
                    if self.collide_array[i, round(j)] == 0:
                        point.a, point.b = i, j
                        return point

    cdef inline bint is_index_valid(self, double i, double j):
        return 0 <= i < SCREEN_WIDTH and 0 <= j < SCREEN_HEIGHT

    cpdef void update(self, center_player):

        self.centerPose = center_player