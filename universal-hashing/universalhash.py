"""
Create a family of universal hash functions.
"""

import random
import math

def isPrime(num):
    if num <= 1:
        return False
    numFactors = 0
    curr = 2
    while curr <= math.sqrt(num):
        if numFactors > 1:
            return False
        while num % curr == 0:
            num /= curr
            numFactors += 1
        curr = 3 if curr == 2 else curr + 2
    if num != 1:
        numFactors += 1
    return numFactors == 1

def baseRep(x, m):
    """
    Return values a0,a1,... such that x = a0 * m^0 + a1 * m^1 + ...
    """
    maxExp = math.floor(math.log(x, m))
    rep = [0] * (maxExp + 1)
    for i in range(maxExp, -1, -1):
        digit = x // (m**i)
        rep[i] = digit
        x %= (m**i)
    return rep

def randVec(r, m):
    """
    Return a = <a0,a1,...,ar>, a vector of r+1 randomly chosen values from the set
    {0,1,...,m-1}
    """
    return [random.randint(0,m-1) for _ in range(r+1)]

def dot(A, B, mod=None):
    out = 0
    for i in range(min(len(A), len(B))):
        out += A[i] * B[i]
        if mod is not None:
            out %= mod
    return out

def universalHash(x, m, hi, a=None):
    """
    
    """
    r = math.floor(math.log(hi, m))
    rep = baseRep(x, m)
    # Pad the base representation to length r+1
    for _ in range(r + 1 - len(rep)):
        rep.append(0)
    
    # Generate a random vector if not passed in
    if a is None:
        a = randVec(r, m)

    return dot(rep, a, mod=m)

if __name__ == "__main__":
    x = int(input())
    m = int(input())
    hi = int(input())
    print(universalHash(x, m, hi))
    print(isPrime(2))

