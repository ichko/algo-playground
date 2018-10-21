from collections import Counter, defaultdict
from math import log2


def entropy(arr):
    probs = [freq / len(arr) for _, freq in Counter(arr).items()]

    return -sum(prob * log2(prob) for prob in probs)


def info_gain(X, y, attrib_id):
    split_vals = Counter([x[attrib_id] for x in X])

    cls_y_vals = defaultdict(lambda: [])
    for id in range(len(X)):
        cls_y_vals[X[id][attrib_id]].append(y[id])

    weighted_entropies = [
        len(y_vals) / len(X) * entropy(y_vals) for _, y_vals in cls_y_vals.items()
    ]

    return entropy(y) - sum(weighted_entropies)


def attr_filter(X, y, attr_id, attr_val):
    valid_ids = list(
        map(
            lambda t: t[0],
            filter(lambda v: v[1] == attr_val, enumerate(map(lambda x: x[attr_id], X))),
        )
    )

    return [X[id] for id in valid_ids], [y[id] for id in valid_ids]


class Rule:
    def fit(self, X, y, unused_attrib_ids):
        self.current_entropy = entropy(y)

        if self.current_entropy == 0:
            self.predict_cls = max(Counter(y).items(), key=lambda x: [1])[0]
            return

        gains = {
            attrib_id: info_gain(X, y, attrib_id) for attrib_id in unused_attrib_ids
        }
        max_gain_attrib_id = max(gains.items(), key=lambda x: x[1])[0]
        unused_attrib_ids.remove(max_gain_attrib_id)

        max_gain_attrib_vals = set(map(lambda x: x[max_gain_attrib_id], X))

        print("Entropy", self.current_entropy)
        print("Atrib gains", gains)
        print("Split by", max_gain_attrib_id, max_gain_attrib_vals)

        self.max_gain_attrib_id = max_gain_attrib_id
        self.splitter = {}

        for attr_val in max_gain_attrib_vals:
            new_X, new_y = attr_filter(X, y, max_gain_attrib_id, attr_val)
            self.splitter[attr_val] = Rule().fit(new_X, new_y, unused_attrib_ids)

    def predict(self, x):
        if self.current_entropy == 0:
            return predict_cls

        return self.splitter[x[self.max_gain_attrib_id]].predict(x)


class ID3:
    def fit(self, X, y):
        self.root = Rule().fit(X, y, set(range(len(X[0]))))


if __name__ == "__main__":
    X = [["T", "T"], ["T", "T"], ["T", "F"], ["F", "F"], ["F", "T"], ["F", "T"]]

    y = [1, 1, 0, 1, 0, 0]

    entropy_example = entropy(y)
    gain_example = info_gain(X, y, 1)

    print(entropy_example)
    print(gain_example)

    X = [
        ["Synny", "Warm", "Normal", "Strong", "Warm", "Same"],
        ["Synny", "Warm", "High", "Strong", "Warm", "Same"],
        ["Rain", "Cool", "High", "Strong", "Warm", "Change"],
        ["Synny", "Warm", "High", "Strong", "Cool", "Change"],
        ["Synny", "Warm", "Normal", "Weak", "Warm", "Same"],
    ]

    y = [1, 1, 0, 1, 0]

    id3 = ID3()
    id3.fit(X, y)
