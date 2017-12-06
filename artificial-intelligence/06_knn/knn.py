from collections import Counter


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

    X = [[1, 1], [2, 2]]
    y = [3.14, 2]
    X_test = [[0, 0]]

    knn = KNN(1)
    knn.fit(X, y)
    y_test = knn.predict(X_test)
    print(y_test)
