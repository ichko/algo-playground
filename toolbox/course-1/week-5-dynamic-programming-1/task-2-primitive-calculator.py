# python3


def min_num_operations(num, inverse_ops):
    num_ops = [0, 0]
    parents = [None, 0]

    for cur_num in range(2, num + 1):
        all_parents = [iop(cur_num) for iop in inverse_ops]
        valid_parents = [int(p) for p in all_parents if float(p).is_integer()]
        min_parent = min(valid_parents, key=lambda p: num_ops[p] + 1)
        parents.append(min_parent)
        num_ops.append(num_ops[min_parent] + 1)

    path = []
    from_id = num
    while parents[from_id] is not None:
        path.append(from_id)
        from_id = parents[from_id]

    return num_ops[-1], path[::-1]


if __name__ == '__main__':
    n = int(input())
    min_num_ops, path = min_num_operations(n, [
        lambda x: x / 2,
        lambda x: x / 3,
        lambda x: x - 1
    ])

    print(min_num_ops)
    print(' '.join(map(str, path)))
