import csv
from functools import reduce
from operator import mul


def read_file(file_name):
  with open(file_name, newline='') as file:
    data = list(csv.reader(file, delimiter=',', quotechar='\n'))
    return [row[1:] for row in data], [row[0] for row in data]


def get_cls_set(data, col):
  return set(row[col] for row in data)


def get_frequency(data, col_cls_list):
  return len(1 for row in range(len(data)) if all(
    row[col] == cls for col, cls in col_cls_list
  ))


def get_probability(data, col_a, col_b):
  frequency = dict()

  for cls_a in get_cls_set(data, col_a):
    for cls_b in get_cls_set(data, col_b):
      frequency[(cls_a, cls_b)] = get_frequency(
        data, [(col_a, cls_a), (col_b, cls_b)]
      )

  return frequency


class NaiveBayes:
  def __init__(self):
    self.probabilities = []
    self.label_classes = None

  def fit(self, X, y):
    data = [x + [y] for x, y in zip(X, y)]
    self.label_classes = get_cls_set(data, -1)
    for col in range(len(data[0])):
      self.probabilities.append(get_probability(data, col, -1))

    return self

  def predict(self, X):
    predictions = []
    for row in X:
      predictions.append(max(
        self.get_cls_prob(row, label_cls), label_cls
          for label_cls in self.label_classes,
        key=lambda k: k[1]
      ))

    return predictions

  def score(self, X, y):
    pass

  def get_cls_prob(self, row, label):
    return reduce(
      mul, [self.probabilities[(row, label)]
            for feature in features], 1
    )


if __name__ == '__main__':
  X, y = read_file('voting.data')

  model = NaiveBayes().fit(X, y)
  score = model.score(X, y)

  print(score)
