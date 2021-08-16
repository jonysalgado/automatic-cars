cdef struct tuple_int_int
cdef struct tuple_tuple_double


cdef class Vector2:
    """
    Represents a bidimensional geometric vector.
    """
    cdef public double x
    cdef public double y

    cdef inline void normalize(self)
    cdef inline double dot(self, Vector2 v)
    cdef inline double magnitude(self)
    cdef inline double rotation(self, double angle)


cdef class Pose:
    """
    Represents a pose on the plane, i.e. a (x, y) position plus a rotation.
    """
    cdef public Vector2 position
    cdef public double rotation

cdef class TransformCartesian:

    cdef double x
    cdef double y

cdef class TransformPolar:
    
    cdef double linear_speed
    cdef double rotation

cdef class function_linear:

    cdef double total_angle, a, b
    cdef Pose centerPos

    cdef inline tuple_int_int calcAB(self)
    cdef inline double y(self, double x)
    cdef inline double x(self, double y)