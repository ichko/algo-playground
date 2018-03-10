# python3


def change(full_sum, denoms):
    sums = [0]
    for current_sum in range(1, full_sum + 1):
        prev_sums = [current_sum - coin for coin in denoms
                     if current_sum - coin >= 0]
        sums.append(min([sums[ps] + 1 for ps in prev_sums]))

    return sums[-1]


if __name__ == '__main__':
    money = int(input())
    print(change(money, [1, 3, 4]))
