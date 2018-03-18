# python3


def max_ammount(W, weights):
    values = [[0 for _ in weights + [0]] for _ in range(W + 1)]
    for w in range(1, W + 1):
        for i, wi in enumerate(weights):
            values[w][i + 1] = max([
                values[w][i],
                values[w - wi][i] + wi if w - wi >= 0 else 0
            ])

    return values[-1][-1]


if __name__ == '__main__':
    capacity, _ = list(map(int, input().split()))
    items = list(map(int, input().split()))

    print(max_ammount(capacity, items))
