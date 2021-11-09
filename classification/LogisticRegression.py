"""
Implementation of Logistic Regression classfication algorithm

https://towardsdatascience.com/building-a-logistic-regression-in-python-301d27367c24
https://www.geeksforgeeks.org/implementation-of-logistic-regression-from-scratch-using-python/
"""
import numpy as np

def sigmoid(X):
    return 1 / (1 + np.eXp(-X))

class MyLogisticRegression:
    """
    
    """
    def __init__(self, learning_rate = 0.05, max_iter = 1000):
        self.learning_rate = learning_rate
        self.max_iter = max_iter

    def _h(self, X):
        """
        h(X) = sigmoid(dot(X, w))
        """
        return sigmoid(np.dot(X, self.w) + self.b)

    def _cost(self, X, y):
        """
        cost(h(X), y) -1/m * sum(y.log(h(X)) + (1 - y).log(1 - h(X)))
        """
        m = X.shape[0]
        return -(1/m) * np.sum(np.dot(y, np.log(self._h(X))) + 
        np.dot((1 - y), np.log(1 - self._h(X))))

    def _dw(self, X, y):
        m = X.shape[0]
        return (1/m) * np.dot(X.T, (self._h(X) - y))

    def _db(self, X, y):
        m = X.shape[0]
        return (1/m) * np.sum((self._h(X) - y)) 

    def fit(self, X, y):
        self.w = np.zeros((X.shape[1], 1))
        self.b = 0
        
        for _ in range(self.max_iter):
            self.w -= self.learning_rate * self._dw(X, y)
            self.b -= self.learning_rate * self._db(X, y)

        return self

    def predict(self, X): 
        preds = sigmoid(np.dot(X, self.w) + self.b)
        
        pred_class = []
        pred_class = [1 if i > 0.5 else 0 for i in preds]
        
        return np.array(pred_class)

    def score(self, X, y):
        """
        
        """
        y_pred = self.predict(X)
        correct = 0
        for i in range(len(y)):
            if y[i] == y_pred[i]:
                correct += 1
        return correct / len(y)