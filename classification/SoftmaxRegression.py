"""
Implementation of softmax regression algorithm for multiclass logistic 
regression

Based on:
https://towardsdatascience.com/multiclass-logistic-regression-from-scratch-9cc0007da372
"""
import numpy as np

"""
Replace softmax/onehot implementation with these for performance increase.
The implemented onehot is not much slower because only called once, but
the scipy softmax is much faster than own implementation and is very 
noticeable because it is called once every iteration, and there are 1000 
iterations.
"""
from scipy.special import softmax
from sklearn.preprocessing import OneHotEncoder
onehot_encoder = OneHotEncoder(sparse=False)

def softmax_row(Z):
    return np.array([np.exp(row)/np.sum(np.exp(row)) for row in Z])

def onehot(Y):
    N = Y.shape[0]
    Y_oh = np.zeros((N, np.max(Y)+1))
    for i in range(N):
        Y_oh[i][Y[i]] = 1
    return Y_oh

class MySoftmaxRegression:
    def __init__(self, max_iter=1000, learning_rate=0.1, lambda_=0.01):
        self.max_iter = max_iter
        self.learning_rate = learning_rate
        self.lambda_ = lambda_
    
    def _loss(self, X, Y_oh, W):
        # Don't bother with the regularisation λ|W|^2 in the loss function,
        # only relevant for the gradient 
        N = X.shape[0]
        return 1/N * (np.trace(X @ W @ Y_oh.T) + \
            np.sum(np.log(np.sum(np.exp(-X @ W), axis=1))))

    def _gradient(self, X, Y_oh, W):
        F = softmax(-X @ W, axis=1)
        # F = softmax_row(-X @ W)
        N = X.shape[0]
        return 1/N * (X.T @ (Y_oh - F)) + 2 * self.lambda_ * W

    def fit(self, X, Y):
        #Y_oh = onehot_encoder.fit_transform(Y.reshape(-1,1))
        Y_oh = onehot(Y)
        self.W = np.zeros((X.shape[1], Y_oh.shape[1]))
        self.losses = []

        for _ in range(self.max_iter):
            self.W -= self.learning_rate * self._gradient(X, Y_oh, self.W)
            self.losses.append(self._loss(X, Y_oh, self.W))

        return self

    def predict(self, X):
        F = softmax(-X @ self.W, axis=1)
        #F = softmax_row(-H @ self.W)
        return np.argmax(F, axis=1)

    def score(self, X, Y):
        Y_pred = self.predict(X)
        correct = 0
        for i in range(len(Y)):
            if Y[i] == Y_pred[i]:
                correct += 1
        return correct / len(Y)