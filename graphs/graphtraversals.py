"""
Implementation of graph traversal algorithms

G = directed or undirected graph
"""
from queue import Queue, LifoQueue
from graphs.directedgraph import DirectedGraph
from graphs.undirectedgraph import UndirectedGraph 

def dfs(G, src, dest):
    """
    Iterative depth-first search using a stack
    """
    nV = G.getNumVertices()
    visited = [-1] * nV
    found = False
    S = LifoQueue(maxsize=nV)

    visited[src] = src
    S.put(src)
    while not found and not S.empty():
        v = S.get()
        if v == dest:
            found = True
        for w in range(nV):
            if G.edgeExists(v, w) and visited[w] == -1:
                visited[w] = v
                S.put(w)
    
    return None if not found else getPath(src, dest, visited)

def bfs(G, src, dest):
    """
    Breadth-first search using a queue
    same as DFS but use a queue instead of a stack
    """
    nV = G.getNumVertices()
    visited = [-1] * nV
    found = False
    Q = Queue(maxsize=nV)

    visited[src] = src
    Q.put(src)
    while not found and not Q.empty():
        v = Q.get()
        if v == dest:
            found = True
        for w in range(nV):
            if G.edgeExists(v, w) and visited[w] == -1:
                visited[w] = v
                Q.put(w)
    
    return None if not found else getPath(src, dest, visited)

def getPath(src, dest, visited):
    """
    Return path of vertices from src to dest assuming that it exists
    """
    path = []
    i = dest
    while i != src:
        path.append(i)
        i = visited[i]
    path.append(src)
    return list(reversed(path))

if __name__ == "__main__":
    G = DirectedGraph(4)
    G.insertEdge(0,1)
    #G.insertEdge(1,3)
    G.insertEdge(1,2)
    G.insertEdge(2,3)
    print(dfs(G,0,3))
    print(bfs(G,0,3))

        
