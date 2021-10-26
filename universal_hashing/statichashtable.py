"""
it doesnt work lol
"""

import math
from universalhash import isPrime, randVec, universalHash

search  =5

class StaticHashTable:
    def __init__(self, hi):
        self.hi = hi
        self.size = self.findTableSize(hi) 
        self.primaryTable = [[] for _ in range(self.size)]
        self.primaryHash = self.randHashFunc()
        self.secondaryHash = [self.randHashFunc() for _ in range(self.size)]
        self.hashTable = [None for _ in range(self.size)]
        self.hash1()
        self.hash2()
    
    @staticmethod
    def findTableSize(n):
        """
        Find a prime number m such that n ≤ m ≤ 2n to be the size of the hash table
        """
        if n == 0 or n == 1:
            return 2
        for m in range(n, 2*n):
            if isPrime(m):
                return m
        return None # should always be able to find an m

    def randHashFunc(self):
        return randVec(math.floor(math.log(self.hi, self.size)), self.size)

    def hash1(self):
        """
        
        """
        # check if sum(n_i^2) < 4n for i from 1 to M
        ni = 5*self.hi
        itt = 1
        while ni >= 4*self.hi:
            if itt > 1:
                self.primaryHash = self.randHashFunc()
            ni = 0
            self.fillPrimaryTable()
            for i in range(self.size):
                ni += len(self.primaryTable[i]) ** 2
            itt += 1

    def fillPrimaryTable(self):
        for i in range(self.size):
            self.primaryTable[i].clear()
        m = self.size
        r = math.floor(math.log(self.hi, m))
        for i in range(1, self.hi+1):
            self.primaryTable[universalHash(i, m, self.hi, self.primaryHash)].append(i)

    def hash2(self):
        for ix in range(self.size):
            self.fillSecondaryTable(ix)

    def fillSecondaryTable(self, ix):
        tix = self.primaryTable[ix]
        m = self.findTableSize(len(tix))
        if m is None:
            self.hashTable[ix] = None
            return
        self.hashTable[ix] = [None] * m
        for i in range(len(tix)):
            # j_x = h_ix(x)
            jx = universalHash(tix[i], m, self.hi, self.secondaryHash[ix])
            if tix[i] == search:
                print(f"{jx} = hash(({tix[i]}, {m}), {self.hi}, {self.secondaryHash[ix]})")
                print()
            if self.hashTable[ix][jx] is None:
                self.hashTable[ix][jx] = tix[i]
            else:
                self.secondaryHash[ix] = self.randHashFunc()
                self.fillSecondaryTable(ix)



if __name__ == "__main__":
    h = StaticHashTable(10)
    print(h.primaryTable)
    print(h.hashTable)
    print(h.size)
    n = universalHash(search, h.size, h.hi, h.primaryHash)
    print(n)
    n = universalHash(search, h.size, h.hi, h.primaryHash)
    print(n)
    n2 = universalHash(search, 2, h.hi, h.secondaryHash[n])
    print(n2)
    n2 = universalHash(search, 2, h.hi, h.secondaryHash[n])
    print(f"{n2} = hash(({search}, {2}), {h.hi}, {h.secondaryHash[n]})")
    print(n2)

        