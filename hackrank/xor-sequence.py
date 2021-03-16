#!/bin/python3
"""
Xor-sequence
SRC - https://www.hackerrank.com/challenges/xor-se/problem

Sample Input 0:
    3
    2 4
    2 8
    5 9

Sample Output 0:
    7
    9
    15
"""

import math
import os
import random
import re
import sys

MAX_BITS = 17


def count_ones(n, bit_id):
    ones_in_group = 2**bit_id
    group_size = ones_in_group * 2
    num_groups = (n + 1) // group_size
    ones_in_groups = num_groups * ones_in_group

    rem_ones = 0
    rem = (n + 1) % group_size
    if rem > group_size // 2:
        rem_ones = rem - group_size // 2

    return ones_in_groups + rem_ones


def get_bit_vector_ones_counts(n, max_bit):
    ones_cnts = []
    for i in range(0, max_bit + 1):
        num_ones = count_ones(n, bit_id=i)
        ones_cnts.append(num_ones)

    return ones_cnts


def A_n(n):
    n_bits = get_bit_vector_ones_counts(n, max_bit=MAX_BITS)
    result = 0
    for i, num_ones in enumerate(n_bits):
        if num_ones % 2 != 0:
            result += 2**i

    return result


def xor_sequence(l, r):
    l_bits = get_bit_vector_ones_counts(l - 1, max_bit=MAX_BITS)
    r_bits = get_bit_vector_ones_counts(r, max_bit=MAX_BITS)

    result = 0
    for i, (l, r) in enumerate(zip(l_bits, r_bits)):
        if (r - l) % 2 != 0:
            result += 2**i

    return result


def xor_sequence_2(l, r):
    result = 0
    for i in range(l + 1, r + 1, 2):
        result ^= i

    if (r - l + 1) % 2 != 0:
        return A_n(r) ^ result

    return result


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input())

    for q_itr in range(q):
        lr = input().split()

        l = int(lr[0])

        r = int(lr[1])

        # a_l = A_n(l)
        # a_r = A_n(r)
        # print('a_l', a_l)
        # print('a_r', a_r)

        result = xor_sequence_2(l, r)

        fptr.write(str(result) + '\n')

    fptr.close()
