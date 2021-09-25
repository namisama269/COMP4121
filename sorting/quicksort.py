from utils import *
#numCalls = 0

def quicksort(A, lo=0, hi=-10):
    if hi == -10:
        hi = len(A)-1

    # base case
    if lo >= hi:
        return

    i = partition(A, lo, hi)
    quicksort(A, lo, i-1)
    quicksort(A, i+1, hi)

def partition(A, lo, hi):
    pivot = A[lo]
    i, j = lo+1, hi

    while True:
        while (A[i] <= pivot and i < j):
            i += 1
        while (pivot < A[j] and j > i):
            j -= 1
        if i == j:
            break
        A[i], A[j] = A[j], A[i]
    

    j = i if A[i] <= pivot else i-1
    A[lo], A[j] = A[j], A[lo]
    return j


def quicksort_show(A, lo = 0, hi = -10, track_sorted=[]):
    #global numCalls
    #numCalls += 1
    #if numCalls > 10:
    #    return

    if len(track_sorted) == 0:
        track_sorted = ['_' for _ in A]

    if hi == -10:
        hi = len(A)-1

    if lo == 0 and hi == len(A)-1:
        print("A = ", end='')
        print(A)
        print(f"lo = {lo}, hi = {hi}")
        print()

    header = f"Quicksort on subarray A[{lo}..{hi}] = {A[lo:hi+1]}"
    print("="*70)
    print(header)
    print(f"Already sorted: ", end='')
    print_list_hl(track_sorted, [], "", "", sep=' ')
    print("="*70)
    print()

    # base case
    if lo >= hi:
        # update which parts of A are sorted if showing exec
        for i in range(max(hi,0), min(len(A)-1, lo+1)):
            if i >= 0 and i < len(A):
                track_sorted[i] = A[i]

        print(TAB*0 + f"Base case lo >= hi reached: {lo} >= {hi}")
        print()
        return

    i = partition_show(A, lo, hi, track_sorted)
    quicksort_show(A, lo, i-1, track_sorted)
    quicksort_show(A, i+1, hi, track_sorted)

def partition_show(A, lo, hi, track_sorted=[]):
    #global numCalls
    #numCalls += 1
    #if numCalls > 10:
    #    return

    pivot = A[lo]
    i, j = lo+1, hi

    print(TAB*0 + f"Partitioning from indices {lo} to {hi}")
    print(TAB*0 + f"pivot = A[{lo}] = {pivot}, i = {i}, j = {j}")
    print()
    
    while True:
        ni = nj = 0
        while (A[i] <= pivot and i < j):
            print(TAB*1 + f"A[{i}] = {A[i]} <= pivot and i < j, incrementing i")
            i += 1
            ni += 1
        while (pivot < A[j] and j > i):
            print(TAB*1 + f"pivot < A[{j}] = {A[j]} and j > i, decrementing j")
            j -= 1
            nj += 1
        if i == j:
            print(TAB*1 + f"Intersection at i = j = {i}, all swaps except pivot done")
            print()
            break
        print()
        if ni == nj == 0:
            print(TAB*1 + f"A[i] = {A[i]} > pivot and A[j] = {A[j]} <= pivot, i and j not changed")
        else:
            print(TAB*1 + f"Incremented i {ni} times, decremented j {nj} times")
        print(TAB*1 + f"i = {i}, j = {j}")
        print(TAB*1 + f"Swapping A[{i}] = {A[i]} and A[{j}] = {A[j]}")
        A[i], A[j] = A[j], A[i]
        print(TAB*2 + f"A[{lo}..{hi}] = {A[lo:hi+1]}")
        print()
    
    
    j = i if A[i] <= pivot else i-1
    if A[i] <= pivot:
        print(TAB*0 + f"A[i] = {A[i]} <= pivot, so swap pivot with intersection index {i} to get all elements left of pivot <= pivot")
    else:
        print(TAB*0 + f"A[i] = {A[i]} > pivot, so swap pivot with index {i-1} before intersection index {i} to get all elements left of pivot <= pivot")
    
    
    print()
    A[lo], A[j] = A[j], A[lo]

    track_sorted[j] = A[j]
    print(TAB*0 + f"Partition index: {j}")
    print(TAB*0 + f"Partitioned subarray A[{lo}..{hi}] around index {j}: ", end='')
    print_list_hl(A[lo:hi+1], [j-lo], "(", ")")
    print(TAB*0 + f"Current A = ", end='')
    print_list_hl(A, [j], "(", ")")
    print()

    return j

if __name__ == "__main__":
    #7 8 4 1 9 3 2 6 5
    #93 42 86 49 85 37 24 53 16 77
    #4 4 4 4 4 4 4 4 4 4
    #A = [int(x) for x in input("Enter items: ").split()]
    A = [x for x in range(500,0,-1)]
    revlist = [1,2,3,4,5]#[x for x in range(5,0,-1)]
    quicksort(A)
    print("="*70)
    print("Sorted: ")
    print("="*70)
    print()
    print(A)
    print()