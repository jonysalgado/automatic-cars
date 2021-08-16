from utils cimport *
from libc.math cimport sqrt, cos, abs, M_PI
from params import SCREEN_WIDTH, SCREEN_HEIGHT, M2PIX, N_SENSORS
import numpy as np
cimport numpy as np
cimport sensors


cdef struct tuple_int_int:
    int a
    int b

cdef struct tuple_tuple_double:
    tuple_int_int a
    double b

cdef class Sensors:

    def __cinit__(self, np.ndarray[long, ndim=2] collide_array,
                       center_player, int number):
        
        self.collide_array = collide_array
        self.centerPose = center_player
        self.number = number
        self.angle = 2*M_PI*number/N_SENSORS

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
        
        cdef double totalAngle, distance
        cdef int centerX, centerY
        cdef tuple_int_int point
        cdef tuple_tuple_double result

        centerY = round(self.centerPose.position.y * M2PIX)
        centerX = round(self.centerPose.position.x * M2PIX)
        totalAngle = self.totalAngle()
        if abs(self.normalAngle(totalAngle) - M_PI/2) < M_PI/180:
            point = self.getFinalPosition(1)
            distance = sqrt((point.a-centerX)**2 + (point.b-centerY)**2)
            result.a, result.b = point, distance
            return result
        
        elif abs(self.normalAngle(totalAngle) - 3*M_PI/2) < M_PI/180:
            point = self.getFinalPosition(2)
            distance = sqrt((point.a-centerX)**2 + (point.b-centerY)**2)
            result.a, result.b = point, distance
            return result

        elif cos(self.normalAngle(totalAngle)) > 0:
            point = self.getFinalPosition(3)
            distance = sqrt((point.a-centerX)**2 + (point.b-centerY)**2)
            result.a, result.b = point, distance
            return result
        
        elif cos(self.normalAngle(totalAngle)) < 0:
            point = self.getFinalPosition(4)
            distance = sqrt((point.a-centerX)**2 + (point.b-centerY)**2)
            result.a, result.b = point, distance
            return result

    cdef inline tuple_int_int getFinalPosition(self, int case):

        cdef int centerX, centerY, j
        cdef tuple_int_int point
        cdef double angle
        angle = self.normalAngle(self.totalAngle())

        centerY = round(self.centerPose.position.y * M2PIX)
        centerX = round(self.centerPose.position.x * M2PIX)
        # angle is 90 degrees
        if case == 1:
            for i in range(centerY, SCREEN_HEIGHT):
                if self.is_index_valid(centerX, i) and self.collide_array[centerX, i] < 0:
                    point.a, point.b = centerX, i
                    return point

        # angle is 270 degrees
        elif case == 2:
            for i in range(centerY, 0, -1):
                if self.is_index_valid(centerX, i) and self.collide_array[centerX, i] < 0:
                    point.a, point.b = centerX, i
                    return point
            
        # angle is between 3*pi/2 and pi/2
        elif case == 3:
            function = function_linear(angle, self.centerPose)
            for i in np.arange(centerX, SCREEN_WIDTH, 0.5):
                j = round(function.y(i))
                if self.is_index_valid(round(i), j) and self.collide_array[round(i), j] < 0:
                    point.a, point.b = round(i), j
                    return point

            if M_PI/4 < angle and angle < 7*M_PI/4:
                if M_PI/4 < angle:
                    for j in range(centerY, SCREEN_HEIGHT):
                        i = round(function.x(j))
                        if self.is_index_valid(i, round(j)) and self.collide_array[i, round(j)] < 0:
                            point.a, point.b = i, round(j)
                            return point
                
                else:
                    for j in range(centerY, 0, -1):
                        i = round(function.x(j))
                        if self.is_index_valid(i, round(j)) and self.collide_array[i, round(j)] < 0:
                            point.a, point.b = i, round(j)
                            return point
            else:
                for i in range(centerX, SCREEN_WIDTH):
                    j = round(function.y(i))
                    if self.is_index_valid(round(i), j) and self.collide_array[round(i), j] < 0:
                        point.a, point.b = round(i), j
                        return point

        # angle is between pi/2 and 3*pi/2
        elif case == 4:
            function = function_linear(angle, self.centerPose)
            if 5*M_PI/4 < angle and angle < 3*M_PI/4:
                if 5*M_PI/4 < angle:
                    for j in range(centerY, SCREEN_HEIGHT):
                        i = round(function.x(j))
                        if self.is_index_valid(i, round(j)) and self.collide_array[i, round(j)] < 0:
                            point.a, point.b = i, round(j)
                            return point
                
                else:
                    for j in range(centerY, 0, -1):
                        i = round(function.x(j))
                        if self.is_index_valid(i, round(j)) and self.collide_array[i, round(j)] < 0:
                            point.a, point.b = i, round(j)
                            return point
            else:
                for i in range(centerX, 0, -1):
                    j = round(function.y(i))
                    if self.is_index_valid(round(i), j) and self.collide_array[round(i), j] < 0:
                        point.a, point.b = round(i), j
                        return point

        point.a, point.b = centerX, centerY
        return point

    cdef inline bint is_index_valid(self, int i, int j):
        return 0 <= i < SCREEN_WIDTH and 0 <= j < SCREEN_HEIGHT

    cpdef void update(self, center_player):

        self.centerPose = center_player