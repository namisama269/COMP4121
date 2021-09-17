import random

def findith(A, i, p=0, r=-1):
    # Update default parameter r
    if r == -1:
        r = len(A)-1
    
    # Error check
    if p > r or i < 1 or i > r-p+1:
        raise ValueError("Invalid parameters")
    
    # Copy the list because it will be modified
    return randselect([_ for _ in A], i, p, r)

def randselect(A, i, p, r):
    """
    Choose the ith smallest element of A[p..r]
    """
    # Base case: A has only 1 element
    if p == r and i == 1:
        return A[p]

    # Randomly select a pivot
    q = random.randint(p, r)

    # Partition A[p..r] so that all elements left of A[q] are <= A[q] and
    # all elements right of A[q] are > A[q]
    # k is equal to how many elements are to the left of A[q]
    k = partition(A, p, r, q)

    if k == i: # If the ith smallest element is the pivot
        return A[p+k-1]
    else: # Continue recursion on only the side that can have the ith element
        if i < k:
            return randselect(A, i, p, p+k-2)
        else: # i > k
            return randselect(A, i-k, p+k, r)
        

def partition(A, p, r, q):
    """
    Partition A[p..r] so that all elements left of A[q] are <= A[q] and
    all elements right of A[q] are > A[q]

    To deal with large number of duplicates, keep track of a flag that denotes whether 
    the current value equal to the pivot will be treated as < or > the pivot.
    """
    eq_flag = [True] # store in a list to allow pointer-like modifications from function

    pivot = A[q]
    swap(A, p, q)
    i, j = p+1, r

    # Without dealing with duplicates using a flag, alg runs much slower on arrays such as 
    # [9] * 1000
    """
    while True:
        while A[i] < pivot and i < j:
            i += 1
        while pivot < A[j] and j > i:
            j -= 1
        if i == j:
            break
        swap(A, i, j)

    j = i if A[i] <= pivot else i-1
    swap(A, p, j)
    return j-p+1
    """

    while True:
        while less(A[i], pivot, eq_flag) and i < j:
            i += 1
        while less(pivot, A[j], eq_flag) and j > i:
            j -= 1
        if i == j:
            break
        swap(A, i, j)

    j = i if less(A[i], pivot, eq_flag) else i-1
    swap(A, p, j)
    return j-p+1

def less(x, y, eq_flag):
    """
    Modified comparison function. Same as < if x and y are different.
    If x and y are equal, x < y if eq_flag is True, x > y if eq_flag is False.
    """
    if x != y:
        return x < y
    flag = eq_flag[0]
    eq_flag[0] = not eq_flag[0]
    return flag

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