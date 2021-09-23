
class UndirectedGraph:
    """
    Undirected, weighted graph using adjacency matrix representation

    Number of vertices is fixed at initialisation
    """
    def __init__(self, nV):
        self.nV = nV
        self.nE = 0
        self.edges = [[None]*nV for _ in range(nV)]

    def getNumVertices(self):
        return self.nV

    def getNumEdges(self):
        return self.nE

    def edgeExists(self, v1, v2):
        return self.edges[v1][v2] is not None

    def insertEdge(self, v1, v2, weight):
        if v1 == v2:
            raise ValueError("Cannot insert self loop")
        if self.edges[v1][v2] is None:
            self.edges[v1][v2] = weight
            self.edges[v2][v1] = weight
            self.nE += 1
    
    def removeEdge(self, v1, v2):
        if v1 == v2:
            raise ValueError("Cannot remove self loop")
        if self.edges[v1][v2] is not None:
            self.edges[v1][v2] = None
            self.edges[v2][v1] = None
            self.nE -= 1

    def displayGraph(self):
        print(f"Graph has {self.nV} vertices and {self.nE} edges")
        print()
        print("Edges: ")
        for i in range(self.nV):
            for j in range(i+1, self.nV):
                if self.edges[i][j] is not None:
                    print(f"edge from {i}-{j} with weight {self.edges[i][j]}")

if __name__ == "__main__":
    g = UndirectedGraph(7)
    g.insertEdge(3,5,10)
    g.insertEdge(3,6,12)
    g.insertEdge(1,4,13)
    g.displayGraph()
    print()
    print(g.edgeExists(5,3))
    print(g.edgeExists(4,3))
    print(g.getNumEdges())
    g.removeEdge(4,1)
    print(g.edgeExists(1,4))
    print(g.getNumEdges())