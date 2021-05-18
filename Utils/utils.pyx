from params import M2PIX
from libc.math cimport round, sqrt, cos, sin, atan, tan, M_PI
cimport utils

cdef struct tuple_double_double:
    double a
    double b

cdef struct tuple_tuple_double:
    tuple_double_double a
    double b


cdef class Vector2:
    """
    Represents a bidimensional geometric vector.
    """
    
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
    
    cdef inline void normalize(self):
        cdef double m = self.magnitude()
        if m == 0:
            self.x = 1
            m = 1
        self.x /= m
        self.y /= m

    cdef inline double dot(self, Vector2 v):
        return self.x * v.x + self.y * v.y

    cdef inline double magnitude(self):
        return sqrt((self.x)**2 + (self.y)**2)

    # padronization: angle in degrees
    cdef inline double rotation(self, double angle):
        return Vector2(self.x*cos(angle), self.y*sin(angle))

cdef class Pose:
    """
    Represents a pose on the plane, i.e. a (x, y) position plus a rotation.
    """

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

    def __cinit__(self, double linear_speed, double rotation):
        self.x = linear_speed * cos(rotation)
        self.y = linear_speed * sin(rotation)


cdef class TransformPolar:

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


    def __cinit__(self, double total_angle, Pose centerPos):
        self.total_angle = total_angle
        self.centerPos = centerPos
        self.a, self.b = self.calcAB().a, self.calcAB().b

    cdef inline tuple_double_double calcAB(self):
        cdef double y0, x0, a, b
        cdef tuple_double_double output
        y0 = round(self.centerPos.position.y  * M2PIX)
        x0 = round(self.centerPos.position.x  * M2PIX)
        a = tan(self.total_angle)
        b = y0 - a*x0
        output.a, output.b = a, b
        return output
    
    cdef inline double y(self, double x):
        return self.a*x + self.b

    cdef inline double x(self, double y):
        return (y - self.b)/self.a
