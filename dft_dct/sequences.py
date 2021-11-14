"""
Operations on 2 sequences A and B
A = [a0,a1,...,an], B = [b0,b1,...,bm]
"""

def add(A, B):
    pass

def pmul(A, B):
    pass

def dot(A, B):
    if len(A) != len(B):
        raise ValueError("A and B must have same length")
    return [A[i]*B[i] for i in range(len(A))]

def concat(A, B):
    pass

def convolution(A, B):
    """
    Brute force linear convolution of 2 sequences
    """
    n = len(A)
    m = len(B)
    conv = [0] * (n+m-1)
    for i in range(n):
        for k in range(m):
            conv[i+k] += A[i]*B[k]
    return conv

def padzero(A, newLen):
    C = A.copy()
    while len(C) < newLen:
        C.append(0)
    return C