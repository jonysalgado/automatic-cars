import numpy as np
cimport numpy as np

cdef class Neural_network:

    cdef public object weights, activations, params, bias
    cdef str activation
    cdef int input_size, output_size
     
    cpdef np.ndarray[double, ndim=1] propagate(self, np.ndarray[double, ndim=1] data)
    cpdef void set_weights(self, object weights)


cdef class Activation_functions:

    cdef str function

    cpdef np.ndarray[double, ndim=1] activate(self, np.ndarray[double, ndim=1] data)
    cdef inline np.ndarray[double, ndim=1] sigmoid(self, np.ndarray[double, ndim=1] data)
    cdef inline np.ndarray[double, ndim=1] relu(self, np.ndarray[double, ndim=1] data)