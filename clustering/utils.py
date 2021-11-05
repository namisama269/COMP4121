import numpy as np

def sq_euclidean(p1, p2):
    """
    
    """
    if len(p1) != len(p2):
        raise ValueError("Points must have equal dimension")
    squared_dist = 0
    for i in range(len(p1)):
        squared_dist += (p2[i] - p1[i])**2
    
    return squared_dist

def euclidean_dist(p1, p2):
    return np.sqrt(sq_euclidean(p1, p2))

def wcss(X, centroids, cluster):
    sum = 0
    for i, val in enumerate(X):
        sum += np.sqrt((centroids[int(cluster[i]), 0]-val[0])**2 +(centroids[int(cluster[i]), 1]-val[1])**2)
        #sum += euclidean_dist(centroids[int(cluster[i])], val)
    return sum

if __name__ == "__main__":
    p1 = np.array([0,0,0])
    p2 = np.array([2,2,2])
    print(euclidean_dist(p1,p2)**2)