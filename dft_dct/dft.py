import cmath
from sequences import padzero, dot, convolution

def p_a(a, k):
    """
    Evaluate the polynomial sum_{l=0 to n-1} (a_l * w_n^lk), where
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
    A = []
    n = len(a)
    for k in range(n):
        A.append(p_a(a, k)) 
    return A

def idft(A):
    """
    IDFT of sequence A = <A_0,A_1,...,A_n-1>
    """
    a = []
    n = len(A)
    for k in range(n):
        a.append(p_a(A, -1*k)/n) 
    return a

def dftConvolution(a, b):
    l = len(a) + len(b) -1
    padzero(a, l)
    padzero(b, l)
    return idft(dot(dft(a), dft(b)))


if __name__ == "__main__":
    a = [int(x) for x in input("Enter sequence a: ").split()]
    b = [int(x) for x in input("Enter sequence b: ").split()]
    actual = convolution(a, b)
    print()

    conv = dftConvolution(a, b)
    ans = []
    for x in conv:
        print(complex(round(x.real,2), round(x.imag,2)))
        ans.append(round(x.real,2))
    print()

    print(ans)
    print(actual)