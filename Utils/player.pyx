from utils cimport *
import numpy as np
cimport numpy as np
from sensors cimport Sensors
from params import *
from libc.math cimport cos, sin, pi
from neural_network cimport Neural_network

cpdef double clamp(double value, double min, double max):
    """
    Clamps a value to keep it within the interval [min, max].

    :param value: value to be clamped.
    :param min: minimum value.
    :param max: maximum value.
    :return: clamped value.
    """
    if value > max:
        return max
    elif value < min:
        return min
    return value

cdef class Player:

    cdef public double linear_speed
    cdef public Pose pose
    cdef public double angular_speed
    cdef public bint bumper_state
    cdef public int number
    cdef public int animationFrame
    cdef public bint controllable
    cdef public double distance
    cdef public object collision_array
    cdef public object sensors
    cdef public object neural_network
    cdef public Pose init_pose

    def __cinit__(self, int number):
        self.linear_speed = 0.0
        self.angular_speed = 0.0
        self.bumper_state = False
        self.number = number
        self.collision_array = None
        self.sensors = None
        self.animationFrame = 1
        self.controllable = False
        self.distance = 0
        self.pose = None
        self.neural_network = None
        self.init_pose = None

    cpdef Pose get_pose(self):
        return self.pose
    
    cpdef void set_pose(self, Pose pose):
        self.init_pose = Pose(pose.position.x, pose.position.y, pose.rotation)
        self.pose = pose
    
    cpdef void init_neural_network(self):
        self.neural_network = Neural_network()


    cpdef void initialSensors(self) except *:
        self.sensors = []
        for i in range(N_SENSORS):
            self.sensors.append(Sensors(self.collision_array, self.pose, i))


    cpdef void set_collision_array(self, np.ndarray[long, ndim=2] collision_array) except *:
        
        self.collision_array = collision_array
        self.initialSensors()

    cpdef void set_velocity(self, double linear_speed, double angular_speed):
        """
        Sets the robot's velocity.

        :param linear_speed: the robot's linear speed.
        :type linear_speed: float
        :param angular_speed: the robot's angular speed.
        :type angular_speed: float
        """
        self.linear_speed = clamp(
            linear_speed, -MAX_LINEAR_SPEED, MAX_LINEAR_SPEED)
        self.angular_speed = clamp(
            angular_speed, -MAX_ANGULAR_SPEED, MAX_ANGULAR_SPEED)

    cpdef void set_bumper_state(self, bint bumper_state):
        """
        Sets the bumper state.

        :param bumper_state: if the bumper has detected an obstacle.
        :type bumper_state: bool
        """
        self.bumper_state = bumper_state

    cpdef bint get_bumper_state(self):
        """
        Obtains the bumper state.

        :return: the bumper state.
        :rtype: bool
        """
        return self.bumper_state

    cpdef void move(self):
        """
        Moves the robot during one time step.
        """
        cdef double dt, v, w

        dt = SAMPLE_TIME
        v = self.linear_speed
        w = self.angular_speed

        if self.bumper_state == True:
            self.set_velocity(0,0)
        else:
            # If the angular speed is too low, the complete movement equation fails due to a division by zero.
            # Therefore, in this case, we use the equation we arrive if we take the limit when the angular speed
            # is close to zero.
            if abs(self.angular_speed) < 1.0e-3:
                self.pose.position.x += v * dt * \
                    cos(self.pose.rotation + w * dt / 2.0)
                self.pose.position.y += v * dt * \
                    sin(self.pose.rotation + w * dt / 2.0)
            else:
                self.pose.position.x += (2.0 * v / w) * \
                    cos(self.pose.rotation + w * dt / 2.0) * sin(w * dt / 2.0)
                self.pose.position.y += (2.0 * v / w) * \
                    sin(self.pose.rotation + w * dt / 2.0) * sin(w * dt / 2.0)
            self.pose.rotation += w * dt

    cpdef void networkController(self, np.ndarray[double, ndim=1] output):

        # move forward
        if output[0] > 0.5:
            self.set_velocity(self.linear_speed + FORWARD_SPEED, self.angular_speed)
        if output[1] > 0.5:
            self.set_velocity(self.linear_speed + BACKWARD_SPEED, self.angular_speed)
        if output[2] > 0.5:
            self.set_velocity(self.linear_speed, self.angular_speed+ANGULAR_SPEED)
        if output[3] > 0.5:
            self.set_velocity(self.linear_speed, self.angular_speed-ANGULAR_SPEED)


    cpdef void userController(self, carsParameters):

        cdef str command

        if len(carsParameters) != 0 and self.number == 0:


            self.set_velocity(0, 0)
            self.controllable = True
            command = carsParameters.pop(0)

            if command == 'up':
                self.set_velocity(FORWARD_SPEED, 0)
            elif command == 'down':
                self.set_velocity(BACKWARD_SPEED, 0)
            
            if command == 'left':
                self.set_velocity(0, -ANGULAR_SPEED)
            elif command == 'right':
                self.set_velocity(0, ANGULAR_SPEED)
    
    cpdef void network_propagate(self):

        cdef object inputNeural, outputNeural
        inputNeural = [sensor.distance()["b"] for sensor in self.sensors]
        inputNeural.append(self.linear_speed*M2PIX)
        inputNeural.append(self.angular_speed)
        outputNeural = self.neural_network.propagate(np.array(inputNeural))
        self.networkController(outputNeural)
    
    cpdef void update(self):
        """
        Updates the robot.
        """
        self.network_propagate()
        self.move()