import random

def find_ith(A, i, p=0, r=-1):
    """
    Find ith smallest element of A[p..r] using randselect
    """
    # Update default parameter r
    if r == -1:
        r = len(A)-1
    
    # Error check
    if p > r or i < 1 or i > r-p+1:
        raise ValueError("Invalid parameters")
    
    # Copy the list because it will be modified
    return randselect(A.copy(), i, p, r)

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
    eq_flag = [True] # Store in a list to allow pointer-like modifications from function

    pivot = A[q]
    swap(A, p, q)
    i, j = p+1, r

    # Without dealing with duplicates using a flag, alg runs much slower on arrays such as 
    # [9] * 1000
    """
    while True:
        while A[i] <= pivot and i < j:
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

def find_ith_det(A, i, p=0, r=-1):
    """
    Find ith element of A[p..r] using deterministic algselect. This algorithm runs asymptotically 
    in linear time but in practice runs much slower than using randselect.
    """
    # Update default parameter r
    if r == -1:
        r = len(A)-1
    
    # Error check
    if p > r or i < 1 or i > r-p+1:
        raise ValueError("Invalid parameters")
    
    # Copy the list because it will be modified
    return algselect(A.copy(), i, p, r)

def algselect(A, i, p=0, r=-1):
    """
    Deterministic version of randselect by finding a suitable pivot using recursion
    """
    # Base case: A has only 1 element
    if p == r and i == 1:
        return A[p]

    # Recursively find a pivot and get its index (of first occurence if there are duplicates)
    pivot = find_pivot(A, p, r)
    q = p + A[p:r+1].index(pivot)

    # Partition A[p..r] so that all elements left of A[q] are <= A[q] and
    # all elements right of A[q] are > A[q]
    # k is equal to how many elements are to the left of A[q]
    k = partition(A, p, r, q)

    if k == i: # If the ith smallest element is the pivot
        return A[p+k-1]
    else: # Continue recursion on only the side that can have the ith element
        if i < k:
            return algselect(A, i, p, p+k-2)
        else: # i > k
            return algselect(A, i-k, p+k, r)

def find_pivot(A, p, r):
    if r-p < 5:
        return A[p+2] if p-r >= 2 else A[r]

    groups = []
    for i in range(p, r+1):
        if (i - p) % 5 == 0:
            groups.append([])
        groups[(i-p)//5].append(A[i])

    medians = []
    for group in groups:
        medians.append(group[2] if len(group) >= 3 else group[-1])

    return find_pivot(medians, 0, len(medians)-1)

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
    print(sorted(A))
    print(find_ith_det(A, i))


#[18, 53, 58, 63, 15, 80, 75, 18, 73, 83] 
# 15 63 24 59 25 94 95 55 88 26 95 36 29 64 37 33 36 89 75 40