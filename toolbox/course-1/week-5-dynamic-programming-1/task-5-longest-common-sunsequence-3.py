# python3


def lcs3(first, second, third):
    memory = [[[0 for _ in range(len(first) + 1)]
               for _ in range(len(second) + 1)]
              for _ in range(len(third) + 1)]

    for f in range(1, len(first) + 1):
        for s in range(1, len(second) + 1):
            for t in range(1, len(third) + 1):
                memory[t][s][f] = max([
                    memory[t - 1][s][f],
                    memory[t][s - 1][f],
                    memory[t][s][f - 1],

                    memory[t - 1][s - 1][f],
                    memory[t - 1][s][f - 1],
                    memory[t][s - 1][f - 1],

                    memory[t - 1][s - 1][f - 1] + 1
                    if first[f - 1] == second[s - 1]
                    and second[s - 1] == third[t - 1]
                    else memory[t - 1][s - 1][f - 1]
                ])

    return memory[-1][-1][-1]


if __name__ == '__main__':
    sequences = []
    _ = input()
    first = list(map(int, input().split()))
    _ = input()
    second = list(map(int, input().split()))
    _ = input()
    third = list(map(int, input().split()))

    print(lcs3(first, second, third))
