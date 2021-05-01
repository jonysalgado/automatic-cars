from params import SCREEN_WIDTH, SCREEN_HEIGHT, FINISH_LINE
import numpy as np
cimport numpy as np
from utils import Vector2

cpdef np.ndarray[int, ndim=2] cost_function(collision_array):

    cdef np.ndarray[double, ndim=2] array = collision_array
    
    cdef np.ndarray[int, ndim=2] cust_array = np.empty(
        (SCREEN_WIDTH, SCREEN_HEIGHT), 
        dtype=int)

    cdef np.ndarray[object, ndim=3] neighbors_array = np.empty(
        (SCREEN_WIDTH, SCREEN_HEIGHT, 8), 
        dtype=object)

    cdef (int, int) node
    cdef np.ndarray[object, ndim=1] neighbors

    # preparing array
    for i in range(SCREEN_WIDTH):
        for j in range(SCREEN_HEIGHT):
            if array[i,j] == 0:
                cust_array[i,j] = -1
                
            else:
                cust_array[i,j] = -2

    queue = []
    cdef (int,int) initialPoint = FINISH_LINE[0]
    cdef (int,int) finishPoint = FINISH_LINE[1] 


    for i in range(initialPoint[0], finishPoint[0] + 1):
        node = (i, initialPoint[1])
        cust_array[node] = 0
        queue.append(node)
    
    while len(queue) != 0:
        node = queue.pop(0)
        neighbors = find_neighbors(node)
        
        for i in range(8):
            if cust_array[neighbors[i]] == -2:
                queue.append(neighbors[i])
                cust_array[neighbors[i]] = cust_array[node] + 100

    return cust_array
     

cpdef np.ndarray[object, ndim=1] find_neighbors((int, int) node):

    cdef np.ndarray[object, ndim=1] neighbors_node = np.empty(
        8, 
        dtype=object)
    cdef int index = 0
    for di in range(-1,2):
            for dj in range(-1,2):
                if is_index_valid(node[0] + di, node[1] + dj):
                    neighbors_node[index] = (node[0] + di, node[1] + dj)
                index += 1
    
    return neighbors_node

cpdef bint is_index_valid(int i, int j):
        return 0 <= i < SCREEN_WIDTH and 0 <= j < SCREEN_HEIGHT