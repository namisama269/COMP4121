"""
Implementation of PageRank algorithm
"""
import sys; sys.path.append("..")
from graphs.directedgraph import DirectedGraph

import numpy as np

def num_outgoing(W, i):
    """
    Number of outgoing links from page i in the web W.
    """
    ans = 0
    for j in range(W.getNumVertices()):
        if W.edgeExists(i, j):
            ans += 1
    return ans

def google_matrix(W, alpha):
    """
    Build the Google matrix from the "web", represented as a
    directed graph where a directed edge from vertex i to j indicates
    that page i has an outgoing link to page j.

    alpha is the damping factor.
    """
    # Build starting G0 matrix
    M = W.getNumVertices()
    G0 = np.zeros((M, M))

    for i in range(M):
        for j in range(M):
            if W.edgeExists(i, j):
                G0[i][j] = 1
        out_links = num_outgoing(W, i)
        if out_links > 0:
            G0[i] /= out_links

    d = np.array([1 if num_outgoing(W, i) == 0 else 0 for i in range(M)]).reshape((M, 1))
    e = np.full((M, 1), 1)

    return alpha*(G0 + 1/M * (d @ e.T)) + (1-alpha)/M * (e @ e.T)

def is_converged(q1, q2, eps):
    """
    Check that 2 vectors are sufficiently close in values.
    """
    if q1 is None or q2 is None:
        return False
    return np.linalg.norm(q1-q2) < eps

def PageRank(W, max_iter=100, damping_factor=0.85, eps=0.001):
    """
    
    """
    # Get the Google matrix for W
    M = W.getNumVertices()
    G = google_matrix(W, damping_factor)

    # Generate a random vector q with all entries between 0 and 1 and sum to 1
    # (probability distribution)
    q = np.random.rand(1, M)
    q /= np.sum(q)

    # Iteratively multiply q by G until convergence or max iterations reached
    q_prev = None
    for i in range(max_iter):
        if is_converged(q_prev, q, eps):
            break
        q_prev = q
        q = q @ G

    # Return the ranks and number of iterations used
    return q, i + 1