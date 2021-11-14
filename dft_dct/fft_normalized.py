"""
Implementation of normalized FFT algorithm.
"""
import math, cmath
from sequences import padzero, dot

def fft_(A):
    n = len(A)
    if n == 1:
        return A

    A0 = [A[i] for i in range(0, len(A), 2)] # even indices
    A1 = [A[i] for i in range(1, len(A), 2)] # odd indices

    # compute FFT* of subproblems of size n/2
    y0 = fft_(A0)
    y1 = fft_(A1)

    # nth root of unity
    w_n = cmath.exp(-2j * cmath.pi / n)
    w = 1

    # combine subproblems
    y = [0] * n
    for k in range(n//2):
        y[k] = y0[k] + w * y1[k]
        y[n//2+k] = y0[k] - w * y1[k]
        w = w * w_n
    
    return y

def ifft_(A):
    n = len(A)
    if n == 1:
        return A

    A0 = [A[i] for i in range(0, len(A), 2)] 
    A1 = [A[i] for i in range(1, len(A), 2)] 

    y0 = ifft_(A0)
    y1 = ifft_(A1)

    # the only difference to FFT* is using exp(2i*pi/n) instead of exp(-2i*pi/n)
    w_n = cmath.exp(2j * cmath.pi / n)
    w = 1

    y = [0] * n
    for k in range(n//2):
        y[k] = y0[k] + w * y1[k]
        y[n//2+k] = y0[k] - w * y1[k]
        w = w * w_n
    
    return y

def fft(A):
    # divide the FFT*(A) by length(A)
    n = cmath.sqrt(len(A))
    return [x/n for x in fft_(A)]

def ifft(A):
    # divide the IFFT*(A) by length(A)
    n = cmath.sqrt(len(A))
    return [x/n for x in ifft_(A)]

def fft_convolution(a, b):
    # the actual length of the convolution
    l = len(a) + len(b) -1

    # for FFT to work, need to pad to first power of 2 that is >= l
    pad = 2 ** (math.ceil(math.log(l, 2)))
    a_pad = padzero(a, pad)
    b_pad = padzero(b, pad)

    # only take up to the actual length of the convolution
    unscaled = ifft(dot(fft(a_pad), fft(b_pad)))

    # because using the normalized FFT, the pointwise multiplication
    # will cause product to be scaled by 1/sqrt(n) * 1/sqrt(n) = 1/n,
    # and the IFFT will multiply by another 1/sqrt(n), so convolution 
    # is scaled by 1/sqrt(n).
    # To fix this, multiply the result by sqrt(n).
    scaled = [x * cmath.sqrt(len(unscaled)) for x in unscaled]

    # only take up to the actual length of the convolution
    return scaled[:l]
