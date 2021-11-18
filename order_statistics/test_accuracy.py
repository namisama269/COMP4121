import random
from randselect import find_ith, find_ith_det

def lib_find_ith(A, i):
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

        output_rand = find_ith(A, i) 
        output_det = find_ith_det(A, i) 
        actual = lib_find_ith(A, i) 
        if output_rand != actual:
            print("Difference found!")
            print(f"find_ith(A, {i}) returned {output_rand}, correct is {actual}")
            break
        else:
            print(f"find_ith(A, {i}) returned {output_rand}, correct is {actual}")
        if output_det != actual:
            print("Difference found!")
            print(f"find_ith_det(A, {i}) returned {output_det}, correct is {actual}")
            break
        else:
            print(f"find_ith_det(A, {i}) returned {output_det}, correct is {actual}")
        
        print(f"Test #{n+1} succeeded!")
        print()

if __name__ == "__main__":
    test_accuracy(10000, -10000, 10000, 200)
    #test_accuracy(1000, -10000, 10000, 200)
