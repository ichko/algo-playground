# python3


def binary_search(sorted_array, query):
    left, right = 0, len(sorted_array)
    while True:
        mid = (left + right) // 2
        if left >= right:
            return -1
        elif query == sorted_array[mid]:
            return mid
        elif query > sorted_array[mid]:
            left = mid + 1
        else:
            right = mid


if __name__ == '__main__':
    sorted_array = list(map(int, input().split()))
    queries = list(map(int, input().split()))
    del sorted_array[0]
    del queries[0]

    # sorted_array = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    # queries = [5]

    queryes_result = []

    for query in queries:
        queryes_result.append(binary_search(sorted_array, query))

    print(' '.join(map(str, queryes_result)))
