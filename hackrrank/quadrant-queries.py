#!/bin/python3

# Problem - <https://www.hackerrank.com/challenges/quadrant-queries/problem>

# cat quadrant-queries.inp | py quadrant-queries.py

import math
import os
import random
import re
import sys

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


def get_points_quad_cnt(points, lr=None):
    if lr is None:
        lr = (0, len(points))

    l, r = lr
    quads = [0, 0, 0, 0]
    for i in range(l, r):
        idx = point_quad_id(points[i])
        quads[idx] += 1

    return quads


def do_a_flip(flip, p):
    x, y = p
    fx, fy = flip
    return [x * fx, y * fy]


def combine_quads(l_quads, r_quads):
    q = [0, 0, 0, 0]
    for i in range(len(l_quads)):
        q[i] = l_quads[i] + r_quads[i]

    return q


class SegTree:
    def update_node(self, node, flip):
        fx, fy = flip
        if fx < 0:
            node = [node[1], node[0], node[3], node[2]]
        if fy < 0:
            node = node[::-1]

        return node

    def combine_flips(self, flip_A, flip_B):
        return [flip_A[0] * flip_B[0], flip_A[1] * flip_B[1]]

    def __init__(self, points):
        n = len(points)
        tree_size = 2 * 2**(math.ceil(math.log2(n)))
        seg_tree = [None] * tree_size
        self.lazy_tree = [[1, 1]] * tree_size

        def recur(l, r, index):
            if l >= r:
                quads = get_points_quad_cnt([points[l]])
                seg_tree[index] = quads
                return quads

            mid = (l + r) // 2
            l_quads = recur(l, mid, 2 * index + 1)
            r_quads = recur(mid + 1, r, 2 * index + 2)

            combined_quads = combine_quads(l_quads, r_quads)
            seg_tree[index] = combined_quads

            return combined_quads

        recur(l=0, r=n - 1, index=0)

        self.seg_tree = seg_tree
        self.n = n

    def flip_lazy_children(self, index, flip):
        l = index * 2 + 1
        r = index * 2 + 2
        if l < len(self.lazy_tree):
            self.lazy_tree[l] = self.combine_flips(self.lazy_tree[l], flip)

        if r < len(self.lazy_tree):
            self.lazy_tree[r] = self.combine_flips(self.lazy_tree[r], flip)

    def lazy_update(self, index):
        lazy_flip = self.lazy_tree[index]
        self.flip_lazy_children(index, lazy_flip)
        node = self.seg_tree[index]
        node = self.update_node(node, lazy_flip)
        self.seg_tree[index] = node
        self.lazy_tree[index] = [1, 1]

    def update(self, ul, ur, flip):
        def recur(l, r, index):
            self.lazy_update(index)

            if ul > r or ur < l:
                return self.seg_tree[index]

            if l >= ul and r <= ur:
                node = self.seg_tree[index]
                node = self.update_node(node, flip)
                self.flip_lazy_children(index, flip)
                self.seg_tree[index] = node
                return node

            mid = (l + r) // 2
            l_quads = recur(l, mid, 2 * index + 1)
            r_quads = recur(mid + 1, r, 2 * index + 2)

            combined_quads = combine_quads(l_quads, r_quads)
            self.seg_tree[index] = combined_quads

            return combined_quads

        recur(0, self.n - 1, 0)

    def query(self, ul, ur):
        def recur(l, r, index):
            self.lazy_update(index)

            if ul > r or ur < l:
                return [0, 0, 0, 0]

            if l >= ul and r <= ur:
                return self.seg_tree[index]

            mid = (l + r) // 2
            l_quads = recur(l, mid, 2 * index + 1)
            r_quads = recur(mid + 1, r, 2 * index + 2)

            combined_quads = combine_quads(l_quads, r_quads)

            return combined_quads

        return recur(0, self.n - 1, 0)


def quadrants(points, queries):
    tree = SegTree(points)
    # print(tree)

    for q in queries:
        c, l, r = q.split(' ')
        l = int(l) - 1
        r = int(r) - 1
        # print(tree.query(0, len(points) - 1))

        if c == 'C':
            quads = tree.query(l, r)
            # quads = [0, 0, 0, 0]
            # for i in range(l, r):
            #     p = points[i]
            #     quads[point_quad_id(p)] += 1

            print(' '.join(map(str, quads)))
        else:
            flip = [1, -1] if c == 'X' else [-1, 1]
            tree.update(l, r, flip)
            # for i in range(l, r):
            #     points[i] = do_a_flip(flip, points[i])


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
