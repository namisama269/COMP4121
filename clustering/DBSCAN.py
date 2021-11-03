"""
Implementation of the DBSCAN (Density-based spatial clustering of applications with noise). Runtime
is a lot slower than the scikit-learn implementation.

Based on:
https://github.com/eriklindernoren/ML-From-Scratch/blob/master/mlfromscratch/unsupervised_learning/dbscan.py
"""
import numpy as np
from utils import euclidean_dist

class MyDBSCAN:
    def __init__(self, eps, min_samples):
        # Radius 
        self.eps = eps
        # Minimum number of points in a cluster
        self.min_samples = min_samples

        # Accessible parameters:
        self.labels = None
        self.num_clusters = None

    def _get_neighbours(self, point_i):
        """
        Get the index of points that are at most eps away from point with index 
        point_i.
        """
        neighbours = []
        for i, point in enumerate(self.data):
            # Distance metric is Euclidean distance
            if euclidean_dist(point, self.data[point_i]) <= self.eps:
                neighbours.append(i)
        return np.array(neighbours)

    def _expand_cluster(self, point_i, neighbours):
        """
        Recursively expand a cluster starting with a point with index point_i
        and its precomputed neighbours.
        """
        # Start with the point itself as the cluster
        cluster = [point_i]

        for nb in neighbours:
            # Only expand from points that have not been visited yet
            if self.visited[nb]:
                continue
            self.visited[nb] = True
            # Get the current neighbour's neighbours
            distant_nbs = self._get_neighbours(nb)
            # If there are sufficient neighbours to form a cluster, continue 
            # expansion along this neighbour
            if len(distant_nbs) >= self.min_samples:
                cluster += self._expand_cluster(nb, distant_nbs)
            # Otherwise, only the neighbour gets added and do not continue
            # expanding
            else:
                cluster.append(nb)
        
        return cluster

    def fit(self, X):
        """
        Fit the data into clusters using DBSCAN.
        """
        n_samples = X.shape[0]
        self.data = X
        self.clusters = []
        # Keep track of which points have been visited when expanding clusters
        self.visited = [False for _ in range(n_samples)]
        # Initially, all points are not labelled so are default to -1 (noise)
        self.labels = np.full(n_samples, -1)
       
        for i in range(n_samples):
            # Try to expand clusters on unvisited points
            if self.visited[i]:
                continue
            # Get the current point's neighbours
            neighbours = self._get_neighbours(i)
            # If there are enough neighbours to form a cluster, continue expansion
            if len(neighbours) >= self.min_samples:
                self.visited[i] = True
                self.clusters.append(self._expand_cluster(i, neighbours))
        
        # Assign labels to each cluster
        cluster_idx = 0
        for cluster in self.clusters:
            if len(cluster) >= self.min_samples:
                for i in cluster:
                    self.labels[i] = cluster_idx
                cluster_idx += 1