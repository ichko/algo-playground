# python3


# TODO: Not working
def majority_divide_and_conquer(array):
    def helper(left, right):
        if right - left == 1:
            return array[left]

        mid = (right + left) // 2
        left_majority = helper(left, mid)
        right_majority = helper(mid, right)
        if left_majority == right_majority:
            return left_majority
        else:
            return -1

    return 0 if helper(0, len(array)) < 0 else 1


def majority_sort(array):
    array.sort()
    counter = 0
    for prev, current in zip(array, array[1:]):
        if prev == current:
            counter += 2 if counter == 0 else 1
        else:
            counter = 0
        if counter > len(array) / 2:
            return 1

    return 0


if __name__ == '__main__':
    _ = input()
    array = list(map(int, input().split()))
    print(majority_sort(array))
