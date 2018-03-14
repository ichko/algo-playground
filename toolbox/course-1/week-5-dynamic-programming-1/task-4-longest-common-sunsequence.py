# python3


def lcs(first_squence, second_sequence):
    prev_row_vals = [0 for _ in first_squence] + [0]
    for sec_el in second_sequence:
        new_row_vals = [0]
        cur_row_prev_val = 0

        for i, fel in enumerate(first_squence):
            cur_row_prev_val = max([
                cur_row_prev_val,
                prev_row_vals[i + 1],
                prev_row_vals[i] + 1 if sec_el == fel else prev_row_vals[i]
            ])
            new_row_vals.append(cur_row_prev_val)
        prev_row_vals = new_row_vals

    return prev_row_vals[-1]


if __name__ == '__main__':
    _ = input()
    first_squence = list(map(int, input().split()))
    _ = input()
    second_sequence = list(map(int, input().split()))

    print(lcs(first_squence, second_sequence))
