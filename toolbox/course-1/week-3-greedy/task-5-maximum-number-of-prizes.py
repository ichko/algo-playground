# Uses python3

if __name__ == '__main__':
    n = int(input())
    sumands = []
    current_sum = 0
    current_sumand = 1

    while current_sum + current_sumand <= n:
        current_sum += current_sumand
        sumands.append(current_sumand)
        current_sumand += 1

    sumands[-1] += n - current_sum

    print(len(sumands))
    print(' '.join(map(str, sumands)))
