"""
Implementation of K-Median clustering algorithm
"""
import numpy as np
import pandas as pd

class MyKMedian:
    def __init__(self, max_iter = 300):
        self.max_iter = max_iter
        # Directly access 
        self.centroids = None
        self.clusters = None

    def metric(self, p1, p2):
        """
        The distance metric used in K-Median clustering is the Manhattan distance
        """
        dist = 0
        for i in range(len(p1)):
            dist += abs(p1[i] - p2[i])
        return dist


    def fit(self, X, k):
        clusters = np.zeros(X.shape[0])

        # select k random centroids
        random_idxs = np.random.choice(len(X), size=k, replace=False)
        centroids = X[random_idxs, :]
        
        i = 0
        while i < self.max_iter:
            # for each point
            for i, point in enumerate(X):
                mn_dist = float('inf')

                # find the min dist of the point from all centroids
                for idx, centroid in enumerate(centroids):
                    d = self.metric(centroid, point)
                    # store closest centroid 
                    if mn_dist > d:
                        mn_dist = d
                        clusters[i] = idx

            # new centroids are found from the mean of all points in each cluster
            new_centroids = pd.DataFrame(X).groupby(by=clusters).median().values

            # if centroids are same then stop
            if np.count_nonzero(centroids-new_centroids) == 0:
                break
            else:
                centroids = new_centroids

        self.centroids = centroids
        self.clusters = clusters
        i += 1