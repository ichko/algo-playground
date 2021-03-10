#!/bin/python3

# Even Tree
# https://www.hackerrank.com/challenges/even-tree/problem

import math
import os
import random
import re
import sys
from collections import defaultdict

# Complete the evenForest function below.


def evenForest(t_nodes, t_edges, t_from, t_to):
    assocs = defaultdict(lambda: [])
    for f, t in zip(t_from, t_to):
        assocs[f].append(t)
        assocs[t].append(f)

    sub_tree_size = defaultdict(lambda: 0)

    def calc_size(node, parent):
        if len(assocs[node]) == 0:
            sub_tree_size[node] = 1
            return 1

        if node in sub_tree_size:
            return sub_tree_size[node]

        for child in assocs[node]:
            if child != parent:
                sub_tree_size[node] += calc_size(child, node)
        sub_tree_size[node] += 1

        return sub_tree_size[node]

    calc_size(node=1, parent=None)

    print('sub_tree_size', dict(sub_tree_size))
    print('assocs', dict(assocs))
    result = 0
    vis = set()

    def bfs(node):
        nonlocal result

        if node in vis or len(assocs[node]) == 0:
            return

        vis.add(node)
        for child in assocs[node]:
            if child not in vis:
                child_subtree_size = sub_tree_size[child]
                parent_compliment_size = t_nodes - child_subtree_size
                if child_subtree_size % 2 == 0 and parent_compliment_size % 2 == 0:
                    print('c', child, node)
                    result += 1

                bfs(child)

    bfs(node=1)

    return result


if __name__ == '__main__':
    fptr = sys.stdout

    t_nodes, t_edges = map(int, input().rstrip().split())

    t_from = [0] * t_edges
    t_to = [0] * t_edges

    for i in range(t_edges):
        t_from[i], t_to[i] = map(int, input().rstrip().split())

    res = evenForest(t_nodes, t_edges, t_from, t_to)

    fptr.write(str(res) + '\n')

    fptr.close()
