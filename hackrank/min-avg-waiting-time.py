#!/bin/python3

# Minimum Average Waiting Time
# https://www.hackerrank.com/challenges/minimum-average-waiting-time/problem

import os
import sys
import heapq


def fill_pq(pq, customers, idx):
    arrival, _ = customers[idx]
    t = arrival
    while idx < len(customers) and customers[idx][0] == arrival:
        heapq.heappush(pq, (customers[idx][1], customers[idx]))
        idx += 1

    return t, idx


#
# Complete the minimumAverage function below.
#
def minimumAverage(customers):
    customers.sort(key=lambda x: x[0])

    pq = []

    t, idx = fill_pq(pq, customers, idx=0)

    waiting_time = 0
    while len(pq) > 0:
        _, (arrival, cook_time) = heapq.heappop(pq)
        t += cook_time
        waiting_time += t - arrival

        while idx < len(customers) and customers[idx][0] < t:
            heapq.heappush(pq, (customers[idx][1], customers[idx]))
            idx += 1

        if len(pq) == 0 and idx < len(customers):
            t, idx = fill_pq(pq, customers, idx=idx)

    return waiting_time // len(customers)


if __name__ == '__main__':
    fptr = sys.stdout

    n = int(input())

    customers = []

    for _ in range(n):
        customers.append(list(map(int, input().rstrip().split())))

    result = minimumAverage(customers)

    fptr.write(str(result) + '\n')

    fptr.close()
