"""
Implementation of randomised Karger's algorithm to find min cut with high probability of accuracy
"""
import sys
sys.path.append('.')

import random
import math

from graphs.undirectedgraph import UndirectedGraph   

INT_MAX = 2147483647

def contract(G, u, v):
    """
    The basic operation in Karger's min cut algorithm.

    Given an edge (u,v), fuse the 2 vertices uv into a single vertex [uv] and replace edges
    (u,x) and (v,x) with a single edge ([uv],x) with weight w([uv],x) = w(u,x) + w(v,x).

    Implemented by returning a new graph with 1 less vertex, [uv] set to highest index and
    all other vertices' indices are shifted down.
    """
    nV = G.getNumVertices()
    G_uv = UndirectedGraph(nV-1)
    uv = nV-2
    edges = G.getEdges()
    
    # Insert edges that do not involve vertices to be fused
    for edge in edges:
        v1, v2, w = edge
        if u != v1 and u != v2 and v != v1 and v != v2:
            G_uv.insertEdge(vertex_contracted_idx(v1, nV, u, v), vertex_contracted_idx(v2, nV, u, v), w)

    # Check all other vertices for an edge incident to both u and v and insert it
    for x in range(nV):
        if x == u or x == v:
            continue
        # Fuse edges from vertices that are incident to u and v
        if G.edgeExists(u, x) and G.edgeExists(v, x):
            G_uv.insertEdge(uv, vertex_contracted_idx(x, nV, u, v), G.getEdgeWeight(u, x) + G.getEdgeWeight(v, x))
        # For edges that are incident to one of u and v but not both, change the endpoint to [uv]
        elif G.edgeExists(u, x):
            G_uv.insertEdge(uv, vertex_contracted_idx(x, nV, u, v), G.getEdgeWeight(u, x))
        elif G.edgeExists(v, x):
            G_uv.insertEdge(uv, vertex_contracted_idx(x, nV, u, v), G.getEdgeWeight(v, x))
    
    return G_uv

def vertex_contracted_idx(x, nV, u, v):
    """
    Return the new vertex index of vertex x in graph with nV vertices in the graph found by
    contracting vertices u and v.
    """
    # The fused vertex [uv] is set to highest index in new graph
    if x == u or x == v:
        return nV-2
    diff = 0
    if x > u:
        diff += 1
    if x > v:
        diff += 1
    return x - diff

def random_edge(G):
    edges = G.getEdges()
    edge = random.choice(edges)
    return edge[0], edge[1]

def _4contract(G):
    """
    4-contract algorithm that contracts a graph to size n/2 4 times, and gets the min
    cut from all 4 subproblems. 

    Runs in O(n^2 log n) and has probability of returning correct min cut > 1/log n. 
    This can be greatly increased for large n by repeating this algorithm and getting
    the minimum result.
    """
    min1 = min2 = min3 = min4 = INT_MAX
    G0 = G.copy()
    V0 = G0.getNumVertices()
    mincut = G0.getEdges()[0][2] if V0 == 2 else INT_MAX
    if V0 > 2:
        # Contract the graph to have V0//2 vertices 4 times
        G1 = G0.copy()
        G2 = G0.copy()
        G3 = G0.copy()
        G4 = G0.copy()

        while G1.getNumVertices() > max(2, V0//2):
            v1, v2 = random_edge(G1)
            G1 = contract(G1, v1, v2)
        while G2.getNumVertices() > max(2, V0//2):
            v1, v2 = random_edge(G2)
            G2 = contract(G2, v1, v2)
        while G3.getNumVertices() > max(2, V0//2):
            v1, v2 = random_edge(G3)
            G3 = contract(G3, v1, v2)
        while G4.getNumVertices() > max(2, V0//2):
            v1, v2 = random_edge(G4)
            G4 = contract(G4, v1, v2)

        min1 = _4contract(G1)
        min2 = _4contract(G2)
        min3 = _4contract(G3)
        min4 = _4contract(G4)
    
    return min(mincut, min1, min2, min3, min4)

def karger(G):
    """
    Run the 4-Contract algorithm log(n)^2 times to get expected probability of correct
    min cut to 1-1/n.
    """
    nV = G.getNumVertices()
    mincut = INT_MAX
    num_runs = math.floor(math.log(nV) ** 2)
    for _ in range(num_runs):
        mincut = min(mincut, _4contract(G))
    return mincut
