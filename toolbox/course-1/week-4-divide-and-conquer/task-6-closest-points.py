# python3

import math
import time
from random import randint


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def fromArr(points):
        return [Point(x, y) for x, y in points]


def naive_min_dist(points):
    return min([dist(a, b) for a in points
                for b in points if a is not b])


def dist(a, b):
    dx = a.x - b.x
    dy = a.y - b.y
    return math.sqrt(dx * dx + dy * dy)


def min_dist_fast(points):
    def recur(x_sort, y_sort):
        if len(x_sort) <= 3:
            return naive_min_dist(x_sort)

        mid_id = len(x_sort) // 2
        mid_x = x_sort[mid_id].x

        left_x = x_sort[:mid_id]
        right_x = x_sort[mid_id:]

        left_x_set = set(left_x)

        left_y = [p for p in y_sort if p in left_x_set]
        right_y = [p for p in y_sort if p not in left_x_set]

        l_dist = recur(left_x, left_y)
        r_dist = recur(right_x, right_y)
        min_dist = min(l_dist, r_dist)

        strip_points = [p for p in y_sort
                        if abs(p.x - mid_x) < min_dist]

        for i in range(0, len(strip_points) - 1):
            neighbors_min_dist = min([dist(strip_points[i], neighbor)
                                      for neighbor in strip_points[i + 1:i + 7]])
            min_dist = min(min_dist, neighbors_min_dist)

        return min_dist

    return recur(
        sorted(points, key=lambda p: p.x),
        sorted(points, key=lambda p: p.y)
    )


def time_test():
    inp_size = 500000
    points = Point.fromArr([(randint(0, 3), randint(0, 3))
                            for _ in range(inp_size)])
    start_time = time.time()

    min_dist_fast(points)

    elapsed = time.time() - start_time
    print('%s \t%s' % (inp_size, elapsed), flush=True)


def test():
    while True:
        points = Point.fromArr([(randint(0, 3), randint(0, 3))
                                for _ in range(70)])
        naive_dist = naive_min_dist(points)
        fast_dist = min_dist_fast(points)
        if naive_dist != fast_dist:
            print('ERROR')
            print(points)
            print('naive %s, fast %s' % (naive_dist, fast_dist))
            break


if __name__ == '__main__':
    # test()
    # time_test()

    number_of_points = int(input())
    points = []
    for _ in range(number_of_points):
        points.append(tuple(map(int, input().split())))
    points = Point.fromArr(points)

    print('{0:.9f}'.format(min_dist_fast(points)))
