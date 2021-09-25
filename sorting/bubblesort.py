from utils import *

def bubblesort(A, lo=0, hi=-1):
    if hi == -1:
        hi = len(A)-1

    for i in range(lo, hi):
        nswaps = 0
        for j in range(hi, i, -1):
            if A[j] < A[j-1]:
                A[j], A[j-1] = A[j-1], A[j]
                nswaps += 1
        # stop early if no more swaps needed
        if nswaps == 0:
            break

def bubblesort_show(A, lo = 0, hi = -1):
    if hi == -1:
        hi = len(A)-1

    print("A = ", end='')
    print(A)
    print(f"lo = {lo}, hi = {hi}")
    print()

    total_swaps = 0
    for i in range(lo, hi):
        print(f"i = {i}")
        print()
        nswaps = 0
        for j in range(hi, i, -1):
            if A[j] < A[j-1]:
                print(TAB*1 + f"j = {j}")
                print()
                print(TAB*1 + f"Swapping A[{j-1}] = {A[j-1]} and A[{j}] = {A[j]}")
                print("     A = ", end='')
                print(A)
                print()
                A[j], A[j-1] = A[j-1], A[j]
                total_swaps += 1
                nswaps += 1
        # stop early if no more swaps needed
        if nswaps == 0:
            print(TAB*1 + "Array is already sorted, no more swaps")
            print()
            break
    return total_swaps

if __name__ == "__main__":
    A = [int(x) for x in input("Enter items: ").split()]
    total_swaps = bubblesort_show(A)
    print("Sorted: ")
    print(A)
    print(f"{total_swaps} swaps used")
    print()