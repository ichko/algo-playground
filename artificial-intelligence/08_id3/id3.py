from collections import Counter, defaultdict
from math import log2


def entropy(arr):
    counter = Counter(arr)
    probs = [freq / len(arr) for _, freq in counter.items()]

    return -sum(prob * log2(prob) for prob in probs)


def info_gain(X, y, attrib):
    split_vals = Counter([x[attrib] for x in X])

    cls_y_vals = defaultdict(lambda: [])
    for id in range(len(X)):
        cls_y_vals[X[id][attrib]].append(y[id])

    weighted_entropies = [
        len(y_vals) * entropy(y_vals) for _, y_vals in cls_y_vals.items()
    ]

    return entropy(y) - sum(weighted_entropies) / len(X)


if __name__ == "__main__":
    X = [["sunny", "windy"], ["sunny", "not windy"], ["cloudy", "windy"]]
    y = [1, 1, 0]

    entropy_example = entropy(y)
    gain_example = info_gain(X, y, 1)

    print(entropy_example)
    print(gain_example)
