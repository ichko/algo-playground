# python3


def edit_distance(from_str, to_str):
    prefix_matrix = [[i + j for i in range(len(from_str) + 1)]
                     for j in range(len(to_str) + 1)]

    for i in range(1, len(from_str) + 1):
        for j in range(1, len(to_str) + 1):
            substitution = prefix_matrix[j - 1][i - 1]
            if from_str[i - 1] != to_str[j - 1]:
                substitution += 1

            prefix_matrix[j][i] = min([
                prefix_matrix[j - 1][i] + 1,
                prefix_matrix[j][i - 1] + 1,
                substitution
            ])

    return prefix_matrix[-1][-1]


if __name__ == '__main__':
    from_str = input()
    to_str = input()

    print(edit_distance(from_str, to_str))
