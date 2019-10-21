import csv
from functools import reduce
from operator import mul
from random import shuffle
from math import ceil


def read_file(file_name):
    with open(file_name, newline='') as file:
        return list(csv.reader(file, delimiter=',', quotechar='\n'))


def xy_split(data):
    return [row[1:] for row in data], [row[0] for row in data]


def get_cls_set(data, col):
    return set(row[col] for row in data)


def get_frequency(data, col_cls_list):
    return len([1 for row in data if all(
        row[col] == cls for col, cls in col_cls_list
    )])


def get_probability(data, col_a, col_b):
    frequency = dict()

    for cls_a in get_cls_set(data, col_a):
        for cls_b in get_cls_set(data, col_b):
            frequency[(cls_a, cls_b)] = get_frequency(
                data, [(col_a, cls_a), (col_b, cls_b)]
            ) / get_frequency(data, [(col_b, cls_b)])

    return frequency


def k_fold_cross_val(model, data, k):
    scores = []
    shuffle(data)
    frame_size = ceil(len(data) / k)
    frames = [data[i * frame_size:(i + 1) * frame_size]
              for i in range(k)]

    for i in range(k):
        X_test, y_test = xy_split(frames[i])
        X_train, y_train = xy_split(sum(frames[:i] + frames[i + 1:], []))
        model.fit(X_train, y_train)
        scores.append(model.score(X_test, y_test))

    return scores


def mean(arr):
    return sum(arr) / len(arr)


class NaiveBayes:
    def __init__(self):
        self.probabilities = []
        self.label_cls_prob = dict()
        self.label_classes = None

    def fit(self, X, y):
        data = [x + [y] for x, y in zip(X, y)]
        self.label_classes = get_cls_set(data, -1)

        for col in range(len(data[0])):
            self.probabilities.append(get_probability(data, col, -1))

        for label_cls in self.label_classes:
            self.label_cls_prob[label_cls] = \
                get_frequency(data, [(-1, label_cls)]) / len(y)

        return self

    def predict(self, X):
        predictions = []
        for row in X:
            predictions.append(max((
                (self.get_cls_prob(row, label_cls), label_cls)
                for label_cls in self.label_classes),
                key=lambda k: k[0]
            )[1])

        return predictions

    def score(self, X, y):
        y_hat = self.predict(X)
        return len([
            1 for y_hat_i, y_i in zip(y_hat, y) if y_hat_i == y_i
        ]) / len(y)

    def get_cls_prob(self, row, label):
        return reduce(
            mul,
            [self.probabilities[i][(val, label)] *
             self.label_cls_prob[label] for i, val in enumerate(row)], 1
        )


if __name__ == '__main__':
    data = read_file('voting.data')

    model = NaiveBayes()
    cross_val_scores = k_fold_cross_val(model, data, k=10)
    cross_val_scores = [round(num, 2) for num in cross_val_scores]

    print('cross validation:\n  ', cross_val_scores)
    print('mean score:\n  ', round(mean(cross_val_scores), 5))

    print('========================')

    nb = NaiveBayes()
