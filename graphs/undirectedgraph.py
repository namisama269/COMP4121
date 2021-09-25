
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

    def getEdgeWeight(self, v1, v2):
        if self.edges[v1][v2] is None:
            raise ValueError("Edge not in graph")
        return self.edges[v1][v2]

    def setEdgeWeight(self, v1, v2, weight):
        if self.edges[v1][v2] is None:
            raise ValueError("Edge not in graph")
        self.edges[v1][v2] = weight
        self.edges[v2][v1] = weight

    def edgeExists(self, v1, v2):
        return self.edges[v1][v2] is not None

    def insertEdge(self, v1, v2, weight):
        if v1 == v2:
            raise ValueError("Cannot insert self loop")
        if self.edges[v1][v2] is not None:
            raise ValueError("Edge already in graph")
        self.edges[v1][v2] = weight
        self.edges[v2][v1] = weight
        self.nE += 1
    
    def removeEdge(self, v1, v2):
        if v1 == v2:
            raise ValueError("Cannot remove self loop")
        if self.edges[v1][v2] is None:
            raise ValueError("Edge not in graph")
        self.edges[v1][v2] = None
        self.edges[v2][v1] = None
        self.nE -= 1

    def printGraph(self):
        print(f"Graph has {self.nV} vertices and {self.nE} edges")
        print()
        print("Edges: ")
        for i in range(self.nV):
            for j in range(i+1, self.nV):
                if self.edges[i][j] is not None:
                    print(f"edge from {i}-{j} with weight {self.edges[i][j]}")

    def copy(self):
        """
        """
        new = UndirectedGraph(self.nV)
        new.nE = self.nE
        new.edges = [[None]*self.nV for _ in range(self.nV)]
        for i in range(self.nV):
            for j in range(self.nV):
                new.edges[i][j] = self.edges[i][j]
        return new

    def importGraph(self, DG):
        """
        Create undirected graph by importing from existing directed graph
        """
        self.nV = DG.nV
        self.nE = DG.nE
        self.edges = [[None] * DG.nV for _ in range(DG.nV)]
        for i in range(DG.nV):
            for j in range(DG.nV):
                self.edges[i][j] = DG.edges[i][j]

def importUDGFromFile(self, filename):
    """
    Import graph from file, no error checks. Format:

    nV
    v1 v2 weight
    ...

    weight = 0 if not given

    Return the graph object.
    """
    f = open(filename, 'r')
    lines = f.readlines()
    nV = int(lines[0])
    UDG = UndirectedGraph(nV)
    for i, line in enumerate(lines):
        if i == 0:
            continue
        line = line.split()
        v1, v2 = int(line[0]), int(line[1])
        wt = 0 if len(line) < 3 else float(line[2])
        UDG.insertEdge(v1, v2, wt)
    f.close()

    return UDG


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