# Imports
import sys
sys.path.append('.')

import numpy as np
import matplotlib.pyplot as plt
from regression.LinearRegression import MyLinearRegression
from sklearn.linear_model import LinearRegression

# generate a random dataset
#np.random.seed(0)
x = np.random.rand(100, 1)
y = 3 + 4 * x + np.random.rand(100, 1)

# try the scikit-learn LinearRegression

# initialise the model
regression_model = MyLinearRegression()

# add the bias term 1 to the training set
m = x.shape[0]
x_train = np.c_[np.ones((m,1)), x]

# fit the data
regression_model.fit(x_train, y)
# predict
y_predict = regression_model.predict(x_train)

# data points
plt.scatter(x, y, s=10)
plt.xlabel('x')
plt.ylabel('y')
# predicted values
plt.plot(x, y_predict, color='r')
plt.show()