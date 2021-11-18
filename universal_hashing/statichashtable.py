"""

"""
import math
import random
from universalhash import is_prime, rand_vec, universal_hash

class UniversalHashFunction:
    def __init__(self, m, U):
        self.m = m
        self.U = U
        r = math.floor(math.log(U, m))
        self.a = rand_vec(r, m)

    def hash_(self, x):
        if x > self.U:
            raise ValueError("x cannot be greater than U")
        return universal_hash(x, self.m, self.U, self.a)


def find_table_size(n):
    """
    Find a prime number m such that n <= m <= 2n to be the size of the hash table
    """
    if n == 0 or n == 1:
        return 2
    for m in range(n, 2*n):
        if is_prime(m):
            return m
    return None


class StaticHashTable:
    def __init__(self, U, keys, values):
        if max(keys) > U:
            raise ValueError("All keys must be less than or equal to U")

        # In a proper hash table these should NOT be stored, but we store them
        # anyway so that they do not need to be passed into function parameters.
        self.keys = keys
        self.values = values

        self.U = U
        self.n = len(keys)
        self.m = find_table_size(self.n)

        self.table = [[] for _ in range(self.m)]

        self.primary_hash_function = None
        self.secondary_hash_functions = [None for _ in range(self.m)]

        self._primary_hash()
        self._secondary_hash()
        
    def _primary_hash(self):
        self.primary_hash_function = UniversalHashFunction(self.m, self.U)
        for key in self.keys:
            hashed = self.primary_hash_function.hash_(key)
            self.table[hashed].append(key)
        
        while (sum([len(self.table[i])**2 for i in range(self.m)]) >= 4 * self.n):
            self._primary_hash()

    def _secondary_hash(self):
        for i in range(self.m):
            inner_keys = self.table[i].copy()
            self._secondary_hash_i(i, inner_keys)
    
    def _secondary_hash_i(self, i, inner_keys):
        ni = len(inner_keys)
        mi = find_table_size(ni**2)
        self.table[i] = [None for _ in range(mi)]

        self.secondary_hash_functions[i] = UniversalHashFunction(mi, self.U)
        
        for key in inner_keys:
            hashed = self.secondary_hash_functions[i].hash_(key)
            if self.table[i][hashed] is not None:
                self.table[i] = [None for _ in range(mi)]
                self._secondary_hash_i(i, inner_keys)
            else:
                # store the key, value pair instead of just the value to 
                # check for nonexistent keys when searching
                self.table[i][hashed] = (key, self.values[self.keys.index(key)])
    
    def search(self, key):
        if key > self.U:
            return None
        
        primary_idx = self.primary_hash_function.hash_(key)
        secondary_idx = self.secondary_hash_functions[primary_idx].hash_(key)

        if self.table[primary_idx][secondary_idx] is None:
            return None
        else:
            stored_key, stored_value = self.table[primary_idx][secondary_idx]
        if stored_key != key:
            return None
        
        return stored_value

    def __repr__(self):
        rep = ""
        for i in range(self.m):
            rep += f"{i}: "
            keys = [x[0] if x is not None else None for x in self.table[i]]
            rep += str(keys)
            if i != self.m-1:
                rep += "\n"
        return rep

    
