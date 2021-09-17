import random

def findith(A, i, p=0, r=-1):
    if r == -1:
        r = len(A)-1
    
    if p > r or i < 1 or i > r-p+1:
        raise ValueError("Invalid parameters")
    
    return randselect([_ for _ in A], i, p, r)

def randselect(A, i, p, r):
    """
    Choose the ith smallest element of A[p..r]
    """
    #print(f"randselect called with params p: {p}, r: {r}")
    #print()

    # Base case: A has only 1 element
    if p == r and i == 1:
        return A[p]

    # Randomly select a pivot
    q = random.randint(p, r)
    #q = 3


    # Partition A[p..r] so that all elements left of A[q] are <= A[q] and
    # all elements right of A[q] are > A[q]
    k = partition(A, p, r, q)

    # k is equal to how many elements are to the left of A[q]

    if k == i: # If the ith smallest element is the pivot
        return A[p+k-1]
    else: # Continue recursion on only the side that can have the ith element
        if i < k:
            #print(f"if i < k, call randselect(A, i, p, p+k-2) = randselect(A, {i}, {p}, {p+k-2})")
            return randselect(A, i, p, p+k-2)
        else: # i > k
            #print(f"if i > k, call randselect(A, i-k, p+k, r) = randselect(A, {i-k}, {p+k}, {r})")
            return randselect(A, i-k, p+k, r)
        """
        print(f"q = {q}, k = {k}, i = {i}")
        
        
        return 777
        """
        

def partition(A, p, r, q):
    """
    Partition A[p..r] so that all elements left of A[q] are <= A[q] and
    all elements right of A[q] are > A[q]
    """
    #print(f"partition called with params p: {p}, r: {r}, q: {q}")
    #print()
    pivot = A[q]
    swap(A, p, q)
    #print(A)
    #print(pivot)
    #print()
    i, j = p+1, r

    while True:
        while A[i] <= pivot and i < j:
            i += 1
        while pivot < A[j] and j > i:
            j -= 1
        if i == j:
            break
        swap(A, i, j)
        #print(A)

    j = i if A[i] <= pivot else i-1
    swap(A, p, j)
    #print()
    #print()
    #print(A)
    #print()

    #print(f"returned k = {j-p+1}")
    #print()
    return j-p+1

def swap(A, i, j):
    """
    Swap A[i] and A[j]
    """
    if i not in range(0, len(A)) or j not in range(0, len(A)):
        raise ValueError("Invalid indices")
    A[i], A[j] = A[j], A[i]


if __name__ == "__main__":
    inp = input("Enter items: ")
    inp = inp.replace("[", "")
    inp = inp.replace("]", "")
    inp = inp.replace(",", "")
    A = [int(x) for x in inp.split()]
    i = int(input("Enter index: "))
    print(findith(A, i))

#[18, 53, 58, 63, 15, 80, 75, 18, 73, 83]