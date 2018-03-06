# python3


def binary_search(sorted_array, query):
    left, right = 0, len(sorted_array)
    while True:
        mid = (left + right) // 2
        if left >= right or query == sorted_array[mid]:
            return mid
        elif query > sorted_array[mid]:
            left = mid + 1
        else:
            right = mid


# TODO: finish implementation (off by smth errors)
def count_number_of_segments(l_segments, r_segments, point):
    lt_left = binary_search(l_segments, point)
    gt_right = len(r_segments) - binary_search(r_segments, point)

    return len(l_segments) - lt_left - gt_right


if __name__ == '__main__':
    segment_cnt, _ = list(map(int, input().split()))
    l_segments = []
    r_segments = []
    for _ in range(segment_cnt):
        l, r = list(map(int, input().split()))
        l_segments.append(l)
        r_segments.append(r)
    points = map(int, input().split())

    l_segments.sort()
    r_segments.sort()

    result = []
    for point in points:
        result.append(count_number_of_segments(
            l_segments,
            r_segments,
            point
        ))

    print(' '.join(map(str, result)))
