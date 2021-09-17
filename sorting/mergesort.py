from utils import *

def mergesort(A, lo = 0, hi = -1, show_exec = False, track_sorted=[]):
    pass

def merge(A, lo, hi):
    pass

if __name__ == "__main__":
    #7 8 4 1 9 3 2 6 5
    #93 42 86 49 85 37 24 53 16 77
    #4 4 4 4 4 4 4 4 4 4
    A = [int(x) for x in input("Enter items: ").split()]
    mergesort(A, show_exec=True)
    print("="*70)
    print("Sorted: ")
    print("="*70)
    print()
    print(A)
    print()