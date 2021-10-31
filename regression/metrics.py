"""

"""

import numpy as np

# mean squared error
def mse(prediction, actual):
    return np.sum((prediction - actual)**2)

# root mean squared error
# m is the number of training examples
def rmse(prediction, actual, m):
    return np.sqrt(mse(prediction, actual)/m)

# sum of square of residuals
def ssr(prediction, actual):
    return np.sum((prediction - actual)**2)

# total sum of squares
def sst(actual):
    return np.sum((actual - np.mean(actual))**2)

# R2 score
def r2_score(prediction, actual):
    return 1 - (ssr(prediction, actual)/sst(actual))

