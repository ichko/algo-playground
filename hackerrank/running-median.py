#!/bin/python3

# Find the Running Median
# https://www.hackerrank.com/challenges/find-the-running-median/problem

import os
import sys
import heapq


#
# Complete the runningMedian function below.
#
def runningMedian(a):
    maxh = []
    minh = []
    result = []

    for i, el in enumerate(a):
        if len(minh) == 0:
            minh.append(el)
        elif minh[0] < el:
            heapq.heappush(minh, el)
        else:
            heapq.heappush(maxh, -el)

        if len(minh) > len(maxh) + 1:
            min_el = heapq.heappop(minh)
            heapq.heappush(maxh, -min_el)
        elif len(maxh) > len(minh) + 1:
            max_el = heapq.heappop(maxh)
            heapq.heappush(minh, -max_el)

        if (i + 1) % 2 == 0:
            med = (minh[0] + (-maxh[0])) / 2
        else:
            med = minh[0] if len(minh) > len(maxh) else -maxh[0]

        result.append(med)

    return result


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    a_count = int(input())

    a = []

    for _ in range(a_count):
        a_item = int(input())
        a.append(a_item)

    result = runningMedian(a)

    fptr.write('\n'.join(map(str, result)))
    fptr.write('\n')

    fptr.close()
