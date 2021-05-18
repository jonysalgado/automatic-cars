import numpy as np

# função de ativação sigmóide
def sigmoid(x):
    return 1.0/(1.0 + np.exp(-x))

def identity(x):
    return x

def step(x):
    if x < 0:
        return 0
    else:
        return 1

def tanh(x):
    return (np.exp(x) - np.exp(-x))/(np.exp(x) + np.exp(-x))

# Rectified Linear Unit
def ReLU(x):
    if x < 0:
        return 0
    elif x < 1000:
        return x
    else:
        return 1000

def LeakyReLU(x):
    if x < 0:
        return 0.01*x
    else:
        return x