#!/bin/python3

"""
Problem - <https://www.hackerrank.com/challenges/quadrant-queries/problem>

Segment Trees - <https://cp-algorithms.com/data_structures/segment_tree.html>

cat quadrant-queries.inp | py quadrant-queries.py
"""

import math
import os
import random
import re
import sys


test_input = """4
1 1
-1 1
-1 -1
1 -1
5
C 1 4
X 2 4
C 3 4
Y 1 2
C 1 3
"""

_old_input = input

def text_to_input(text):
    inp_gen = iter(text.split('\n'))

    def new_input():
        return next(inp_gen)

    return new_input

with open('quadrant-queries.inp') as f:
    content = f.read()
input = text_to_input(content)

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
    if x > 0 and y > 0: return 0
    if x < 0 and y > 0: return 1
    if x < 0 and y < 0: return 2
    if x > 0 and y < 0: return 3
    return -1


def combine_quads(out, l_quads, r_quads):
    out[0] = l_quads[0] + r_quads[0]
    out[1] = l_quads[1] + r_quads[1]
    out[2] = l_quads[2] + r_quads[2]
    out[3] = l_quads[3] + r_quads[3]


def update_node(node, flip):
        if flip & 0b10:
            a, b, c, d = node
            node[0] = b
            node[1] = a
            node[2] = d
            node[3] = c
        if flip & 0b01:
            a, b, c, d = node
            node[0] = d
            node[1] = c
            node[2] = b
            node[3] = a


def flip_lazy_children(lazy_tree, index, flip):
    id2 = index * 2
    l = id2 + 1
    r = id2 + 2

    if r < len(lazy_tree):
        lazy_tree[r] ^= flip
    if l < len(lazy_tree):
        lazy_tree[l] ^= flip



def recur_update(seg_tree, lazy_tree, ul, ur, l, r, index, flip):
    lazy_flip = lazy_tree[index]
    node = seg_tree[index]

    if lazy_flip & 0b11:
        update_node(node, lazy_flip)
        flip_lazy_children(lazy_tree, index, lazy_flip)
        lazy_tree[index] = 0b00

    if ul > r or ur < l:
        return node

    if l >= ul and r <= ur:
        update_node(node, flip)
        flip_lazy_children(lazy_tree, index, flip)
        return node

    mid = (l + r) // 2
    id2 = index * 2

    l_quads = recur_update(
        seg_tree, lazy_tree,
        ul, ur, l, mid, id2 + 1, flip
    )

    r_quads = recur_update(
        seg_tree, lazy_tree,
        ul, ur, mid + 1, r, id2 + 2, flip
    )

    combine_quads(node, l_quads, r_quads)
    return node


def recur_query(result, seg_tree, lazy_tree, ul, ur, l, r, index):
    if ul > r or ur < l:
        return

    lazy_flip = lazy_tree[index]
    node = seg_tree[index]

    if lazy_flip & 0b11:
        flip_lazy_children(lazy_tree, index, lazy_flip)
        update_node(node, lazy_flip)
        lazy_tree[index] = 0b00

    if l >= ul and r <= ur:
        result[0] += node[0]
        result[1] += node[1]
        result[2] += node[2]
        result[3] += node[3]
        return

    mid = (l + r) // 2
    id2 = index * 2

    recur_query(
        result, seg_tree, lazy_tree,
        ul, ur, l, mid, id2 + 1
    )
    recur_query(
        result, seg_tree, lazy_tree,
        ul, ur, mid + 1, r, id2 + 2
    )


def recur_build(points, seg_tree, l, r, index):
    node = seg_tree[index]
    if l >= r:
        idx = point_quad_id(points[l])
        node[idx] = 1
        return node

    mid = (l + r) // 2
    id2 = index * 2
    l_quads = recur_build(points, seg_tree, l, mid, id2 + 1)
    r_quads = recur_build(points, seg_tree, mid + 1, r, id2 + 2)

    combine_quads(node, l_quads, r_quads)
    return node


no_flip = 0b00
flip_y = 0b01
flip_x = 0b10
flip_both = 0b11
import numpy as np

def quadrants(points, queries):
    n = len(points)
    tree_size = 2 * 2**(math.ceil(math.log2(n)))
    seg_tree = [[0, 0, 0, 0] for _ in range(tree_size)]
    lazy_tree = [0b00 for _ in range(tree_size)]
    last_idx = n - 1

    recur_build(points, seg_tree, l=0, r=last_idx, index=0)
    result = [0, 0, 0, 0]

    for q in queries:
        c, l, r = q.split(' ')
        l = int(l) - 1
        r = int(r) - 1

        if c == 'C':
            result[0] = 0
            result[1] = 0
            result[2] = 0
            result[3] = 0

            recur_query(
                result, seg_tree, lazy_tree,
                l, r, 0, last_idx, 0
            )

            sys.stdout.write(
                f'{result[0]} {result[1]} {result[2]} {result[3]}\n'
            )
        else:
            if c == 'X':
                recur_update(
                    seg_tree, lazy_tree,
                    l, r, 0, last_idx, 0, flip_y
                )
            else:
                recur_update(
                    seg_tree, lazy_tree,
                    l, r, 0, last_idx, 0, flip_x
                )

        # print(tree.seg_tree)
        # print(tree.lazy_tree)


if __name__ == '__main__':
    import time

    n = int(input().strip())
    p = []

    for _ in range(n):
        p.append(list(map(int, input().rstrip().split())))
    q = int(input().strip())

    queries = []
    for _ in range(q):
        queries_item = input()
        queries.append(queries_item)

    tic = time.perf_counter()

    quadrants(p, queries)

    toc = time.perf_counter()
    print(f'Execution took {toc - tic:0.4f} seconds')
