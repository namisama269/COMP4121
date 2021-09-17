import random
from randselect import findith 

def lib_findith(A, i):
    """
    Find ith element by using library sort on the list and directly accessing the 
    required index, no error checking
    """
    B = A.copy()
    B.sort()
    return B[i-1]

def test_accuracy(array_size, min_val, max_val, num_runs):
    for n in range(num_runs):
        A = [random.randint(min_val, max_val) for __ in range(array_size)]
        i = random.randint(1, array_size)

        output = findith(A, i) 
        actual = lib_findith(A, i) 
        if output != actual:
            print("Difference found!")
            print(f"findith(A, {i}) returned {output}, correct is {actual}")
            print()
            break
        else:
            print(f"findith(A, {i}) returned {output}, correct is {actual}")
            print(f"Test #{n+1} succeeded!")
            print()

if __name__ == "__main__":
    test_accuracy(10000, -10000, 10000, 200)
