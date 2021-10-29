"""
Test gradient descent to find global minimum of a quadratic

https://towardsdatascience.com/implement-gradient-descent-in-python-9b93ed7108d1
"""

# polynomial is ax^2 + bx + c
a = 3
b = 12
c = 5

# make sure the x-coordinate START has a point on the polynomial
START = 0

PRECISION = 0.000001
MAX_ITERATIONS = 10000

LEARNING_RATE = 0.05

# the value of 1st derivative evaluated at x 
# equal to 2ax + b
def gradient(x):
    return 2*a*x + b

def find_min_using_gd():
    # keep track of the change in x between iterations
    # if it goes under the precision then can consider it
    # negligible and can stop
    dx = 1 

    # number of iterations
    i = 1
    curr = START

    while dx > PRECISION and i < MAX_ITERATIONS:
        print(f"Iteration {i}")
        print(f"x = {curr}")

        # save the previous value to compute the change
        prev = curr
        
        # go in the direction of the negative of the gradient
        # because the gradient is the direction of steepest ascent
        # => negative is the direction of steepest descent to find the min
        curr = curr - LEARNING_RATE * gradient(prev)

        dx = abs(curr - prev)
        i += 1


if __name__ == "__main__":
    find_min_using_gd()
        