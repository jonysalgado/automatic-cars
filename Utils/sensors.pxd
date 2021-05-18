from utils cimport *

cdef class Sensors:

    cdef int number
    cdef double angle
    cdef public object collide_array
    cdef public Pose centerPose

    cdef inline double totalAngle(self)
    cdef inline double normalAngle(self, double angle)
    cpdef tuple_tuple_double distance(self)
    cdef inline tuple_double_double getFinalPosition(self, int case)
    cdef inline bint is_index_valid(self, double i, double j)
    cpdef void update(self, center_player)