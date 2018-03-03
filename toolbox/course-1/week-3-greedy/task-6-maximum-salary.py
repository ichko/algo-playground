# Uses python3
from functools import cmp_to_key


def comparator(a, b):
    ab = a + b
    ba = b + a

    return int(ab) - int(ba)


if __name__ == '__main__':
    _ = input()
    digits = input().split()
    digits.sort(key=cmp_to_key(comparator), reverse=True)
    print(''.join(digits))
