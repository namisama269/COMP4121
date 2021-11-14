"""
Implementation of Discrete Fourier Transform (DFT) algorithm for finding
convolutions.

Does not use numpy.
"""
import cmath
from sequences import padzero, dot, convolution

def p_a(a, k):
    """
    Evaluate the polynomial sum_{l=0}^{n-1} (a_l * w_n^lk), where
    w_n is the primitive nth root of unity
    j is reserved for representing i
    """
    n = len(a)
    ans = 0
    for l in range(n):
        ans += a[l] * cmath.exp(-2j * cmath.pi * k * l / n)
    return ans

def dft(a):
    """
    DFT of sequence a = <a_0,a_1,...,a_n-1>
    """
    n = len(a)
    return [p_a(a, k) for k in range(n)]

def idft(A):
    """
    IDFT of sequence A = <A_0,A_1,...,A_n-1>
    """
    n = len(A)
    return [p_a(A, -k) / n for k in range(n)]

def dft_convolution(a, b):
    """
    Compute the convolution of a and b using DFT
    """
    l = len(a) + len(b) -1
    a_pad = padzero(a, l)
    b_pad = padzero(b, l)
    return idft(dot(dft(a_pad), dft(b_pad)))


if __name__ == "__main__":
    a = [int(x) for x in input("Enter sequence a: ").split()]
    b = [int(x) for x in input("Enter sequence b: ").split()]
    actual = convolution(a, b)
    print()

    conv = dft_convolution(a, b)
    ans = []
    for x in conv:
        ans.append(round(x.real,2))

    print(ans)
    print(actual)