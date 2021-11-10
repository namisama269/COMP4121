"""

"""
import numpy as np
#import pandas as pd

def class_count(Y):
    """
    Count the number of each class in vector Y
    """
    counts = {}
    for y in Y:
        if y not in counts:
            counts[y] = 1
        else:
            counts[y] += 1
    return counts

def is_numeric(x):
    return isinstance(x, int) or isinstance(x, float)

class Question:
    """
    
    """
    def __init__(self, col, val):
        self.col = col
        self.val = val
    
    def match(self, example):
        example_val = example[self.col]
        if is_numeric(example_val):
            return example_val >= self.val
        else:
            return example_val == self.val

class LeafNode:
    def __init__(self, Y):
        self.predictions = class_count(Y)

class DecisionNode:
    def __init__(self, question, true_child, false_child):
        self.question = question
        self.true_child = true_child
        self.false_child = false_child

class MyDecisionTree():
    def __init__(self):
        pass

    def _partition(self, X, Y, q):
        """
        
        """
        X_t, X_f = [], []
        Y_t, Y_f = [], []
        for i in range(len(X)):
            if q.match(X[i]):
                X_t.append(X[i])
                Y_t.append(Y[i])
            else:
                X_f.append(X[i])
                Y_f.append(Y[i])
        return np.array(X_t), np.array(Y_t), np.array(X_f), np.array(Y_f)

    def _gini(self, Y):
        """
        
        """
        #counts = pd.Series(Y).value_counts()
        counts = class_count(Y)
        N = Y.shape[0]
        impurity = 1
        for count in counts.values():
            impurity -= (count / N) ** 2
        return impurity

    def _info_gain(self, X_t, Y_t, X_f, Y_f, curr_uc):
        """
        
        """
        p = X_t.shape[0] / (X_t.shape[0] + X_f.shape[0])
        return curr_uc - p * self._gini(Y_t) - (1 - p) * self._gini(Y_f)

    def _opt_partition(self, X, Y):
        """
        Find the question that gives the most info gain if it is used to
        partition the data.
        """
        opt_ig = 0
        opt_q = None
        curr_uc = self._gini(Y)
        M = X.shape[1]
        
        for m in range(M):
            unique_vals = np.unique(X[:, m])
            for val in unique_vals:
                q = Question(m, val)
                
                # split dataset
                X_t, Y_t, X_f, Y_f = self._partition(X, Y, q)
                
                # skip if no split
                if X_t.shape[0] == 0 or Y_t.shape[0] == 0:
                    continue
                    
                ig = self._info_gain(X_t, Y_t, X_f, Y_f, curr_uc)
                
                # just use >
                if ig > opt_ig:
                    opt_ig, opt_q = ig, q
                    
        return opt_ig, opt_q

    def _make_tree(self, X, Y):
        ig, q = self._opt_partition(X, Y)
        
        # can't ask a question
        if ig == 0:
            return LeafNode(Y)
        
        X_t, Y_t, X_f, Y_f = self._partition(X, Y, q)
        
        # recursively make true/false child
        child_t = self._make_tree(X_t, Y_t)
        child_f = self._make_tree(X_f, Y_f)
        
        # can ask questions so this is a decision node
        return DecisionNode(q, child_t, child_f)

    def _print_tree(self, node, spacing=""):
        # Base case: we've reached a leaf
        if isinstance(node, LeafNode):
            print (spacing + "Predict", node.predictions)
            return

        # Print the question at this node
        print (spacing + str(node.question))

        # Call this function recursively on the true branch
        print (spacing + '--> True:')
        self._print_tree(node.true_child, spacing + "  ")

        # Call this function recursively on the false branch
        print (spacing + '--> False:')
        self._print_tree(node.false_child, spacing + "  ")

    def fit(self, X, Y):
        """
        
        """
        # build the tree
        self.tree = self._make_tree(X, Y)

    def _classify(self, row, node):
        if isinstance(node, LeafNode):
            return node.predictions

        if node.question.match(row):
            return self._classify(row, node.true_child)
        else:
            return self._classify(row, node.false_child)

    def predict(self, X):
        final_preds = []
        for ex in X:
            prediction = self._classify(ex, self.tree)
            # find the one with the largest
            opt_pred = None
            opt_count = 0
            for pred, count in prediction.items():
                if count > opt_count:
                    opt_pred, opt_count = pred, count
            final_preds.append(opt_pred)

        return np.array(final_preds)

    def score(self, X, Y):
        Y_pred = self.predict(X)
        correct = 0
        for i in range(len(Y)):
            if Y[i] == Y_pred[i]:
                correct += 1
        return correct / len(Y)