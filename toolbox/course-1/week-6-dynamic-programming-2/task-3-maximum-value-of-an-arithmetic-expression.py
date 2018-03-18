# python3

import math


def max_val_expr(numbers, operations, ops_map):
    min_vals = {(i, i): n for i, n in enumerate(numbers)}
    max_vals = {(i, i): n for i, n in enumerate(numbers)}

    def minMax(i, j):
        min_val, max_val = math.inf, -math.inf
        for t in range(i, j):
            op = ops_map[operations[t]]

            vals = [
                op(max_vals[(i, t)], max_vals[(t + 1, j)]),
                op(max_vals[(i, t)], min_vals[(t + 1, j)]),
                op(min_vals[(i, t)], max_vals[(t + 1, j)]),
                op(min_vals[(i, t)], min_vals[(t + 1, j)])
            ]

            min_val = min([min_val] + vals)
            max_val = max([max_val] + vals)

        return min_val, max_val

    for s in range(1, len(numbers) + 1):
        for i in range(0, len(numbers) - s):
            min_vals[(i, i + s)], max_vals[(i, i + s)] = minMax(i, i + s)

    return max_vals[(0, len(numbers) - 1)]


if __name__ == '__main__':
    expression = input()
    numbers = [int(d) for d in expression[::2]]
    operations = expression[1::2]

    max_val = max_val_expr(numbers, operations, {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b
    })

    print(max_val)
