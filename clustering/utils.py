import sys
sys.path.append('.')

import numpy as np

def euclidean_dist(p1, p2):
    return np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)