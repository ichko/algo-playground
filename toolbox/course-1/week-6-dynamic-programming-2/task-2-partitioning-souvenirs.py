# python3


def knapsack(capacity, weights, values):
    table = [[0 for _ in range(capacity + 1)] for _ in range(len(values) + 1)]

    for w in range(1, capacity + 1):
        for i in range(1, len(values) + 1):
            table[i][w] = max([
                table[i - 1][w - weights[i - 1]] + values[i - 1]
                if w - weights[i - 1] >= 0 else 0,
                table[i - 1][w]
            ])

    take_items_indexes = []
    current_capacity = capacity

    for i in range(len(values), 0, -1):
        if table[i][current_capacity] != table[i - 1][current_capacity]:
            take_items_indexes.append(i - 1)
            current_capacity -= weights[i - 1]

    return take_items_indexes, table[-1][-1]


def is_partitionable(weights, values):
    total_value = sum(values)
    single_knapsack_size = total_value // 3

    if total_value / 3 == single_knapsack_size:
        for _ in range(3):
            items_taken, items_weight = knapsack(
                single_knapsack_size, weights, values
            )

            if items_weight != single_knapsack_size:
                return 0

            new_values = []
            new_weights = []

            for i in items_taken:
                new_values.append(values[i])
                new_weights.append(weights[i])

            values = new_values
            items_weight = new_weights

        return 1

    return 0


if __name__ == '__main__':
    _ = input()
    values = list(map(int, input().split()))
    weights = values[::]

    print(is_partitionable(weights, values))
