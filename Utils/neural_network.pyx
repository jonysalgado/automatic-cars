import numpy as np
cimport numpy as np
cimport neural_network
from params import *
from libc.math cimport sqrt

cdef class Neural_network:

    def __cinit__(self):
        self.weights = []
        self.bias = []
        self.activations = []
        for layer in NEURAL_PARAMS:
            input_size = layer[0]
            output_size = layer[1]
            activation = layer[2]
            # self.weights.append(np.random.randn(input_size,output_size))
            factor = np.random.choice([-1,1], size=(input_size,output_size))
            weights = np.multiply(factor, np.random.uniform(0, 1000, (input_size,output_size)))
            self.weights.append(weights)
            # self.bias.append(3*np.random.randn(output_size))
            self.bias.append(np.zeros(output_size))
            self.activations.append(Activation_functions(activation))


    cpdef np.ndarray[double, ndim=1] propagate(self, np.ndarray[double, ndim=1] data):

        cdef object input_data, z, a, yhat
        input_data = data
        for i in range(len(self.weights)):
            z = np.dot(input_data,self.weights[i]) + self.bias[i]
            a = self.activations[i].activate(z)
            input_data = a
        yhat = input_data
        return yhat

    cpdef void set_weights(self, object weights):
        self.weights = weights


cdef class Activation_functions:

    def __cinit__(self, str name):
        self.function = name

    cpdef np.ndarray[double, ndim=1] activate(self, np.ndarray[double, ndim=1] data):
        if self.function == "sigmoid":
            return self.sigmoid(data)
        elif self.function == "relu":
            return self.relu(data)

    
    cdef inline np.ndarray[double, ndim=1] sigmoid(self, np.ndarray[double, ndim=1] data):
        return 1/(1 + np.exp(data))

    cdef inline np.ndarray[double, ndim=1] relu(self, np.ndarray[double, ndim=1] data):
        return np.maximum(data, np.zeros(data.shape[0]))