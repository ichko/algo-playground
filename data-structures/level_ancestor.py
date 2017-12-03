"""
    Level Ancestor Problem (LA)
"""
from collections import defaultdict as dd
import operator as o, functools as ft


def count_sort(arr, key=lambda k: k):
    data = dd(lambda: [])
    for i in range(len(arr)):
        dd[key(i)].append(arr[i])
    return ft.reduce(o.concat, [])


def set_leaves(node, level=0):
    node.level = level
    if node.is_leaves():
        self.leaves.append(node)
    for child in node.children:
        set_leaves(child, level + 1)


class Node:
    def __init__(self, value, children = []):
        self.value = value
        self.children = set(children)
        self.level = 0

    def add(self, children):
        self.children.update(children)

    def is_leave(self):
        return len(self.children) == 0


class Tree:
    def __init__(self, root):
        self.root = root
        self.leaves = []

    def preprocess(self):
        set_leaves(self.root)
        self.leaves = count_sort(self.leaves, lambda l: l.level)


    def level_ancestor(node, level):
        pass


if __name__ == '__main__':
    n = Node(4)
    r = Node(
        0,
        [Node(1, Node(3, n)), Node(2)]
    )
    t = Tree(t)
    t.preprocess()
    print(t.level_ancestor(n, 2))