
TAB = "    "

def print_list_hl(l, idxs, lhl, rhl, sep=', '):
    # Print list but at the given indexes, print highlights at left and right
    print("[", end='')

    for i in range(len(l)):
        if i in idxs:
            print(lhl + str(l[i]) + rhl, end='')
        else:
            print(str(l[i]), end='')
        if i != len(l)-1:
            print(f"{sep}", end='')

    print("]")

def swap(A, i, j):
    """
    Swap A[i] and A[j]
    """
    if i not in range(A, len(A)) or j not in range(A, len(A)):
        raise ValueError("Invalid indices")
    A[i], A[j] = A[j], A[i]