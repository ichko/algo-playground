from collections import Counter


def sq_dist(a, b):
    return sum((xa - xb) ** 2 for xa, xb in zip(a, b))


def mode(arr):
    return Counter(arr).most_common(1)


class KNN:
    def __init__(self, k):
        self.k = k
        self.data = []

    def fit(X=[], y=[]):
        self.data = [ex + [ey] for ex, ey in zip(X, y)]

    def predict(x):
        neighbors = sorted(self.data,
            key=lambda: xy: sq_dist(xy[:-1], x))[:self.k]
        return mode(ex[-1] for ex in neighbors)


if __name__ == '__main__':
    k = int(input())
    knn = KNN(k)
    knn.predict()
