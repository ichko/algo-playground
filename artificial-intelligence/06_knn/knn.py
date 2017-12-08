from collections import Counter
import csv
from random import shuffle


def xy_split(data):
    return [x[0:-1] for x in data], \
           [x[-1] for x in data]


def read_file(file_name):
    with open(file_name, newline='') as file:
        data = list(csv.reader(file, delimiter=',', quotechar='\n'))
        X, y = xy_split(data)
        return [[float(el) for el in row] for row in X], y


def stratify_split(X, y, test_size):
    data = list(zip(X, y))
    shuffle(data)

    test_X, test_y = xy_split(data[:test_size])
    train_X, train_y = xy_split(data[test_size:])

    return train_X, train_y, test_X, test_y


def sq_dist(a, b):
    return sum((xa - xb) ** 2 for xa, xb in zip(a, b))


def mode(arr):
    return Counter(arr).most_common(1)[0][0]


class KNN:
    def __init__(self, k):
        self.k = k
        self.data = []

    def fit(self, X=[], y=[]):
        self.data = [ex + [ey] for ex, ey in zip(X, y)]
        return self

    def predict(self, X=[]):
        y = []
        for x in X:
            neighbors = sorted(self.data,
                key=lambda xy: sq_dist(xy[:-1], x))[:self.k]
            y.append(mode([ex[-1] for ex in neighbors]))

        return y

    def score(self, X, y):
        y_hat = self.predict(X)
        return sum(int(y_hat_i == y_i)
            for y_hat_i, y_i in zip(y_hat, y)) / len(y)


if __name__ == '__main__':
    # k = int(input())

    X, y = read_file('iris.txt')
    train_X, train_y, test_X, test_y = stratify_split(X, y, 20)

    knn = KNN(10)
    knn.fit(train_X, train_y)

    score = knn.score(test_X, test_y)
    print(score)
