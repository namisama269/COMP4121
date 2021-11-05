"""

"""
import numpy as np
from utils import euclidean_dist, sq_euclidean
from scipy.spatial import distance
from scipy import linalg
from KMeans import MyKMeans
from sklearn.cluster import KMeans

class MySpectralClustering():
    def __init__(self, gamma, eps=0):
        self.gamma = gamma
        self.eps = eps
        # 
        self.num_clusters = 0
        self.labels = None

    def _set_rbf_weighted_matrix(self):
        """
        Compute the weighted adjacency matrix by computing the
        radial basis function (RBF) kernel function:
            exp(-gamma * squared Euclidean distance) for each pair of
            points in the dataset
        gamma = 1/(2 * delta^2)
        """
        dist_pairs = distance.cdist(self.X, self.X, metric="sqeuclidean")
        self.W = np.exp(-self.gamma * dist_pairs)

    def _set_eps_nb_weighted_matrix(self):
        """
        
        """
        pass

    def _set_knn_weighted_matrix(self):
        """
        
        """
        pass

    def _set_degrees_matrix(self):
        """
        Compute the degrees matrix from the weighted adjacency matrix
        using the formula:
        D[i][i] = sum(W[i][j] for all j)
        """
        n = self.X.shape[0]
        self.D = np.zeros((n, n))
        # 1-dimensional array of size n
        degrees = self.W.sum(axis=1)
        for i in range(n):
            self.D[i][i] = degrees[i]

    def _set_laplacian(self):
        """
        Compute the Laplacian matrix L, which is equal to D-W
        """
        self._set_degrees_matrix()
        self.L = self.D - self.W

    def fit(self, X, k):
        self.X = X

        # maybe allow other ways to make weighted matrix later
        self._set_rbf_weighted_matrix()

        # update the Laplacian matrix
        self._set_laplacian()

        evals, evecs = linalg.eig(self.L, left=False, right=True)
        sort_idxs = np.argsort(evals)
        evals = evals[sort_idxs]
        evecs = evecs[:,sort_idxs]
        evecs = np.real(evecs)

        self.evals = evals
        self.evecs = evecs
        
        """
        kmeans = MyKMeans()
        kmeans.fit(evecs[:,0:k], k)

        self.labels = kmeans.clusters.copy()
        """
        self.labels = KMeans(n_clusters=k).fit_predict(evecs[:,0:k])
        
        
