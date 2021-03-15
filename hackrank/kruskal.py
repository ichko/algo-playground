#!/bin/python3
"""

Kruskal (MST): Really Special Subtree
SRC - https://www.hackerrank.com/challenges/kruskalmstrsub/problem

input
4 6
1 2 5
1 3 3
4 1 6
2 4 7
3 2 4
3 4 5

out:
12
"""
import math
import os
import random
import re
import sys

#
# Complete the 'kruskals' function below.
#
# The function is expected to return an INTEGER.
# The function accepts WEIGHTED_INTEGER_GRAPH g as parameter.
#

#
# For the weighted graph, <name>:
#
# 1. The number of nodes is <name>_nodes.
# 2. The number of edges is <name>_edges.
# 3. An edge exists between <name>_from[i] and <name>_to[i]. The weight of the edge is <name>_weight[i].
#
#
from collections import defaultdict


class Node:
    def __init__(self, val, rank=0, parent=None):
        self.val = val
        self.rank = rank
        self.parent = parent


class DisjointSets:

    def __init__(self):
        self.val_to_node = {}

    def add_set(self, val):
        self.val_to_node[val] = Node(val)

    def in_same_set(self, left, right):
        l_node = self.find(left)
        r_node = self.find(right)

        return l_node == r_node

    def find(self, val):
        if val not in self.val_to_node:
            return None

        def recur(node):
            if node.parent is None:
                return node

            node.parent = recur(node.parent)
            return node.parent

        node = self.val_to_node[val]
        return recur(node)

    def union(self, left, right):
        l_node = self.find(left)
        r_node = self.find(right)

        if l_node == r_node:
            return

        if l_node.rank > r_node.rank:
            r_node.parent = l_node
        else:
            l_node.parent = r_node
            r_node.rank = \
                r_node.rank + 1 if r_node.rank == l_node.rank else r_node.rank


def kruskals(g_nodes, g_from, g_to, g_weight):
    edges = []
    for f, t, w in zip(g_from, g_to, g_weight):
        edges.append((f, t, w))

    edges.sort(key=lambda x: x[0] + x[1])
    edges.sort(key=lambda x: x[2])

    print('e', edges)

    node_sets = DisjointSets()
    for node in range(g_nodes):
        node_sets.add_set(node + 1)

    result = 0
    for (f, t, w) in edges:
        if not node_sets.in_same_set(f, t):
            node_sets.union(f, t)
            f_v = node_sets.find(f).val
            t_v = node_sets.find(t).val
            print('edge', f, t, f_v, t_v)
            result += w

    return result


if __name__ == '__main__':
    fptr = sys.stdout

    g_nodes, g_edges = map(int, input().rstrip().split())

    g_from = [0] * g_edges
    g_to = [0] * g_edges
    g_weight = [0] * g_edges

    for i in range(g_edges):
        g_from[i], g_to[i], g_weight[i] = map(int, input().rstrip().split())

    res = kruskals(g_nodes, g_from, g_to, g_weight)

    fptr.write(str(res) + '\n')

    fptr.close()
