#!/bin/python3
"""
Problem - <https://www.hackerrank.com/challenges/quadrant-queries/problem>

Segment Trees - <https://cp-algorithms.com/data_structures/segment_tree.html>

cat quadrant-queries.inp | py quadrant-queries.py

This solution got me 100 points ran with the Pypy2 interpreter
"""

from array import array
import math
import os
import random
import re
import sys

# def profile(func):
#     import cProfile
#     import io
#     import pstats
#     from pstats import SortKey

#     def wrapper(*args, **kwargs):
#         pr = cProfile.Profile()
#         pr.enable()
#         retval = func(*args, **kwargs)
#         pr.disable()
#         s = io.StringIO()
#         sortby = SortKey.CUMULATIVE  # 'cumulative'
#         ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#         ps.print_stats()
#         print(s.getvalue())
#         return retval

#     return wrapper

# test_input = """4
# 1 1
# -1 1
# -1 -1
# 1 -1
# 5
# C 1 4
# X 2 4
# C 3 4
# Y 1 2
# C 1 3
# """

# _old_input = input

# def text_to_input(text):
#     inp_gen = iter(text.split('\n'))

#     def new_input():
#         return next(inp_gen)

#     return new_input

# with open('quadrant-queries.inp') as f:
#     content = f.read()
# input = text_to_input(content)

# input = text_to_input(test_input)

#
# Complete the 'quadrants' function below.
#
# The function accepts following parameters:
#  1. 2D_INTEGER_ARRAY p
#  2. STRING_ARRAY queries
#


def point_quad_id(p):
    x, y = p
    if x > 0 and y > 0:
        return 0
    if x < 0 and y > 0:
        return 1
    if x < 0 and y < 0:
        return 2
    if x > 0 and y < 0:
        return 3
    return -1


def combine_quads(out, l_quads, r_quads):
    out[0] = l_quads[0] + r_quads[0]
    out[1] = l_quads[1] + r_quads[1]
    out[2] = l_quads[2] + r_quads[2]
    out[3] = l_quads[3] + r_quads[3]


def update_node(node, lazy_tree, index, flip):
    a, b, c, d = node

    if flip == 3:
        node[0] = c
        node[1] = d
        node[2] = a
        node[3] = b
    elif flip & 0b10:
        node[0] = b
        node[1] = a
        node[2] = d
        node[3] = c
    elif flip & 0b01:
        node[0] = d
        node[1] = c
        node[2] = b
        node[3] = a

    id2 = index << 1
    l = id2 + 1
    r = id2 + 2

    if r < tree_size:
        lazy_tree[l] ^= flip
        lazy_tree[r] ^= flip
    elif l < tree_size:
        lazy_tree[l] ^= flip


def recur_update(seg_tree, lazy_tree, ul, ur, l, r, index, flip):
    lazy_flip = lazy_tree[index]
    node = seg_tree[index]

    if l >= ul and r <= ur:
        if lazy_flip & 0b11:
            final_flip = lazy_flip ^ flip
        else:
            final_flip = flip
        if final_flip & 0b11:
            update_node(node, lazy_tree, index, final_flip)
        lazy_tree[index] = 0b00
        return node

    if lazy_flip & 0b11:
        update_node(node, lazy_tree, index, lazy_flip)
        lazy_tree[index] = 0b00

    if ul > r or ur < l:
        return node

    mid = l + r
    mid >>= 1
    index <<= 1

    l_quads = recur_update(seg_tree, lazy_tree, ul, ur, l, mid, index + 1,
                           flip)

    r_quads = recur_update(seg_tree, lazy_tree, ul, ur, mid + 1, r, index + 2,
                           flip)

    combine_quads(node, l_quads, r_quads)
    return node


def recur_query(result, seg_tree, lazy_tree, ul, ur, l, r, index):
    if ul > r or ur < l:
        return

    lazy_flip = lazy_tree[index]
    node = seg_tree[index]

    if lazy_flip & 0b11:
        update_node(node, lazy_tree, index, lazy_flip)
        lazy_tree[index] = 0b00

    if l >= ul and r <= ur:
        result[0] += node[0]
        result[1] += node[1]
        result[2] += node[2]
        result[3] += node[3]
        return

    mid = l + r
    mid >>= 1
    index <<= 1

    recur_query(result, seg_tree, lazy_tree, ul, ur, l, mid, index + 1)
    recur_query(result, seg_tree, lazy_tree, ul, ur, mid + 1, r, index + 2)


def recur_build(points, seg_tree, l, r, index):
    node = seg_tree[index]
    if l >= r:
        idx = point_quad_id(points[l])
        node[idx] = 1
        return node

    mid = l + r
    mid >>= 1
    index <<= 1
    l_quads = recur_build(points, seg_tree, l, mid, index + 1)
    r_quads = recur_build(points, seg_tree, mid + 1, r, index + 2)

    combine_quads(node, l_quads, r_quads)
    return node


no_flip = 0b00
flip_y = 0b01
flip_x = 0b10
flip_both = 0b11
tree_size = None


# @profile
def quadrants(points, queries):
    # from io import StringIO
    # file_str = StringIO()

    n = len(points)
    global tree_size
    tree_size = 2 * 2**(math.ceil(math.log(n, 2)))
    tree_size = int(tree_size)
    seg_tree = [array('H', [0, 0, 0, 0]) for _ in xrange(tree_size)]
    lazy_tree = array('b', [0b00 for _ in xrange(tree_size)])
    last_idx = n - 1

    recur_build(points, seg_tree, l=0, r=last_idx, index=0)

    for q in queries:
        c, l, r = q.split(' ')
        l = int(l) - 1
        r = int(r) - 1

        if c == 'C':
            result = [0, 0, 0, 0]

            recur_query(result, seg_tree, lazy_tree, l, r, 0, last_idx, 0)

            out = '%i %i %i %i' % (result[0], result[1], result[2], result[3])
            # file_str.write(out)
            print out
        else:
            if c == 'X':
                recur_update(seg_tree, lazy_tree, l, r, 0, last_idx, 0, flip_y)
            else:
                recur_update(seg_tree, lazy_tree, l, r, 0, last_idx, 0, flip_x)

        # print(tree.seg_tree)
        # print(tree.lazy_tree)

    # print(file_str.getvalue())


if __name__ == '__main__':
    # import time

    n = input()
    p = []

    for _ in range(n):
        t = sys.stdin.readline().strip().split()
        p.append((int(t[0]), int(t[1])))
    q = input()

    queries = []
    for _ in range(q):
        # queries_item = input()
        t = sys.stdin.readline()
        queries.append(t)

    # tic = time.perf_counter()

    quadrants(p, queries)

    # toc = time.perf_counter()
    # print(f'Execution took {toc - tic:0.4f} seconds')
