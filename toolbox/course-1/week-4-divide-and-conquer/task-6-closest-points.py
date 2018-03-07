# python3

import math


def naive_min_dist(points):
    min_dist = math.inf
    for a in points:
        for b in points:
            if a is not b:
                min_dist = min(min_dist, dist(a, b))

    return min_dist


def dist(a, b):
    ax, ay = a
    bx, by = b
    return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)


def min_dist(points):
    points.sort(key=lambda p: p[0])
    y_sorted_points = sorted(points, key=lambda p: p[1])

    def recur(x_sorted_points):
        if len(x_sorted_points) <= 3:
            return naive_min_dist(x_sorted_points)

        mid_id = len(x_sorted_points) // 2
        mid_x = sum([p[0] for p in x_sorted_points]) / len(x_sorted_points)

        l_dist = recur(x_sorted_points[:mid_id])
        r_dist = recur(x_sorted_points[mid_id:])
        min_dist = min(l_dist, r_dist)

        strip_points = [p for p in y_sorted_points
                        if dist(p, (mid_x, p[1])) <= min_dist]

        for i in range(0, len(strip_points), 7):
            neighbors_min_dist = naive_min_dist(strip_points[i:i + 7])
            min_dist = min(min_dist, neighbors_min_dist)

        return min_dist

    return recur(points)


if __name__ == '__main__':
    number_of_points = int(input())
    points = []
    for _ in range(number_of_points):
        points.append(tuple(map(int, input().split())))

    print('{0:.9f}'.format(min_dist(points)))
