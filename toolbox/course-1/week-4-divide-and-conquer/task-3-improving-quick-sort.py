# python3

from random import randint


def quick_sort(array):
    def partition3(left, right):
        pivot = array[left]
        lt, gt = left, left
        for current in range(left + 1, right + 1):
            if array[current] == pivot:
                gt += 1
                array[gt], array[current] = array[current], array[gt]
            elif array[current] < pivot:
                array[lt], array[current] = array[current], array[lt]
                array[gt + 1], array[current] = array[current], array[gt + 1]
                gt += 1
                lt += 1

        return lt, gt

    def recur(left, right):
        if left >= right:
            return

        rand_id = randint(left, right)
        array[left], array[rand_id] = array[rand_id], array[left]

        pivot_lt, pivot_gt = partition3(left, right)
        recur(left, pivot_lt - 1)
        recur(pivot_gt + 1, right)

    recur(0, len(array) - 1)


if __name__ == '__main__':
    _ = input()
    array = list(map(int, input().split()))
    quick_sort(array)
    print(' '.join(map(str, array)))
