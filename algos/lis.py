# python3


def lis(elements):
    """Longest increasing subsequence."""

    n = len(elements)

    max_lis_id = 0
    max_lis_len = 1
    lis_lens = [1] * n
    predecessor = [-1] * n
    result = []

    # Calculate lis values
    for i in range(1, n):
        for j in range(i):
            current_lis_len = lis_lens[j] + 1

            if elements[i] > elements[j] and lis_lens[i] < current_lis_len:
                lis_lens[i] = current_lis_len
                predecessor[i] = j

                if max_lis_len < current_lis_len:
                    max_lis_len = current_lis_len
                    max_lis_id = i

    # Reconstruct the sequence
    for _ in range(max(lis_lens)):
        result.append(elements[max_lis_id])
        max_lis_id = predecessor[max_lis_id]

    return result[::-1]


if __name__ == '__main__':
    elements = list(map(int, input().split()))
    solution = lis(elements)

    print(solution)
