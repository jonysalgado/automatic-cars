from params import M2PIX
from libc.math cimport sqrt, cos, sin, atan, tan, M_PI

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


cdef class Vector2:
    """
    Represents a bidimensional geometric vector.
    """
    cdef double x
    cdef double y
    
    def __cinit__(self, double x, double y):
        """
        Creates a bidimensional geometric vector.

        :param x: x coordinate.
        :type x: float
        :param y: y coordinate.
        :type y: float
        """
        self.x = x
        self.y = y
    
    cpdef void normalize(self) except *:
        cdef double m = self.magnitude()
        if m == 0:
            self.x = 1
            m = 1
        self.x /= m
        self.y /= m

    cpdef double dot(self, Vector2 v) except *:
        return self.x * v.x + self.y * v.y

    cpdef double magnitude(self) except *:
        return sqrt((self.x)**2 + (self.y)**2)

    # padronization: angle in degrees
    cpdef double rotation(self, double angle) except *:
        return Vector2(self.x*cos(angle), self.y*sin(angle))

cdef class Pose:
    """
    Represents a pose on the plane, i.e. a (x, y) position plus a rotation.
    """
    cdef Vector2 position
    cdef double rotation

    def __cinit__(self, double x, double y, double rotation):
        """
        Creates a pose on the plane.

        :param x: x coordinate.
        :type x: float
        :param y: y coordinate.
        :type y: float
        :param rotation: rotation around z axis.
        :type rotation: float
        """
        self.position = Vector2(x, y)
        self.rotation = rotation

cdef class TransformCartesian:

    cdef double x
    cdef double y

    def __cinit__(self, double linear_speed, double rotation):
        self.x = linear_speed * cos(rotation)
        self.y = linear_speed * sin(rotation)


cdef class TransformPolar(object):
    
    cdef double linear_speed
    cdef double rotation

    def __cinit__(self, double x, double y):
        self.linear_speed = sqrt(x**2 + y**2)
        if x > 1.0e-03:
            self.rotation = atan(y/x)
        elif y > 0:
            self.rotation = M_PI
        else:
            self.rotation = -1*M_PI
        if x < 0:
            self.rotation += M_PI



cdef class function_linear:

    cdef double total_angle
    cdef Pose centerPos

    def __cinit__(self, double total_angle, Pose centerPos):
        self.total_angle = total_angle
        self.centerPos = centerPos
        self.a, self.b = self.calcAB()
        # print("a,b, total:",self.a,self.b, self.total_angle)

    def calcAB(self):
        y0 = round(self.centerPos.position.y  * M2PIX)
        x0 = round(self.centerPos.position.x  * M2PIX)
        a = tan(self.total_angle)
        b = y0 - a*x0
        return a, b
    
    def y(self, x):
        return self.a*x + self.b

    def x(self, y):
        return (y - self.b)/self.a
