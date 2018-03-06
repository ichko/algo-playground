# python3


def count_inversions(array):
    def inversions_merge(left, right):
        result = []
        l, r = 0, 0
        inversions = 0

        while l < len(left) and r < len(right):
            if left[l] > right[r]:
                result.append(right[r])
                r += 1
                inversions += len(left) - l
            else:
                result.append(left[l])
                l += 1

        for i in range(l, len(left)):
            result.append(left[i])

        for i in range(r, len(right)):
            result.append(right[i])

        return inversions, result

    def recur(arr):
        if len(arr) == 1:
            return 0, arr

        mid = len(arr) // 2
        left_inv, left_arr = recur(arr[:mid])
        right_inv, right_arr = recur(arr[mid:])
        new_inv, new_arr = inversions_merge(left_arr, right_arr)

        return left_inv + right_inv + new_inv, new_arr

    inversions, _ = recur(array)
    return inversions


if __name__ == '__main__':
    _ = input()
    array = list(map(int, input().split()))
    print(count_inversions(array))
