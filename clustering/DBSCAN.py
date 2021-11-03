"""

https://github.com/eriklindernoren/ML-From-Scratch/blob/master/mlfromscratch/unsupervised_learning/dbscan.py
"""
import numpy as np
from utils import euclidean_dist

class MyDBSCAN:
    def __init__(self, eps, min_samples):
        self.eps = eps
        self.min_samples = min_samples
        self.labels = None
        self.num_clusters = None

    def _get_neighbours(self, point_i):
        neighbours = []
        for i, point in enumerate(self.data):
            if euclidean_dist(point, self.data[point_i]) <= self.eps:
                neighbours.append(i)
        return np.array(neighbours)

    def _expand_cluster(self, point_i, neighbours):
        cluster = [point_i]

        for nb in neighbours:
            if self.visited[nb]:
                continue
            self.visited[nb] = True
            distant_nbs = self._get_neighbours(nb)
            if len(distant_nbs) >= self.min_samples:
                cluster += self._expand_cluster(nb, distant_nbs)
            else:
                cluster.append(nb)
        
        return cluster

    def fit(self, X):
        n_samples = X.shape[0]
        self.data = X
        self.clusters = []
        self.visited = [False for _ in range(n_samples)]
        self.labels = np.full(n_samples, -1)
       
        for i in range(n_samples):
            if self.visited[i]:
                continue
            neighbours = self._get_neighbours(i)
            if len(neighbours) >= self.min_samples:
                self.visited[i] = True
                self.clusters.append(self._expand_cluster(i, neighbours))
        
        for j, cluster in enumerate(self.clusters):
            for i in cluster:
                self.labels[i] = j