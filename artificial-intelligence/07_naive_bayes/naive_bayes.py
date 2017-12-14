import csv


def read_file(file_name):
    with open(file_name, newline='') as file:
        data = list(csv.reader(file, delimiter=',', quotechar='\n'))
        return [row[1:] for row in data], [row[0] for row in data]


def get_categories(data, column):
    return set(row[column] for row in data)


class NaiveBayes:
    def __init__(self):
        pass

    def fit(self, X, y):
        pass

    def predict(self, X):
        pass

    def score(self, X, y):
        pass


if __name__ == '__main__':
    X, y = read_file('voting.data')
    print(y)
