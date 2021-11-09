"""
Implementation of Linear Regression using gradient descent
https://towardsdatascience.com/linear-regression-using-python-b136c91bf0a2


"""
import numpy as np

class MyLinearRegression:
    """
    
    """

    def __init__(self, learning_rate = 0.05, num_iters = 1000):
        self.learning_rate = learning_rate
        self.num_iters = num_iters

    def fit(self, x, y):
        self.costs = []
        self.weights = np.zeros((x.shape[1], 1))
        m = x.shape[0]

        for _ in range(self.num_iters):
            prev_y = np.dot(x, self.weights)
            residuals = prev_y - y
            gradient = np.dot(x.T, residuals)
            self.weights -= 1/m * self.learning_rate * gradient
            cost = 1/(2*m) * np.sum((residuals ** 2))
            self.costs.append(cost)

        return self

    def predict(self, x):
        return np.dot(x, self.weights)