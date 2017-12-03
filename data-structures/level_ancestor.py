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


def get_leaves(node):
    if node.is_leaves():
        yield node
    for child in node.children:
        yield from set_leaves(child)


def max_path_decompose(sorted_leaves, root):
    paths = [[]]
    in_path = dd(lambda: True)
    for leave in sorted_leaves:
        node = leave
        while node is not root and not in_path[node]:
            in_path[node] = True
            paths[-1].append(node)
            node = node.parent

    return paths


def ladder_decompose(paths, root):
    ladders = []
    for path in paths:
        ladder = []
        node = path[0]
        while node is not root and len(ladder) <= 2 * len(path):
            ladder.append(node)
            node = node.parent
            
        laders.append(ladder)

    return ladders


class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.children = set()
        self.level = 0

    def add(self, children):
        self.children.update(children)
        for child in children:
            child.level = self.level + 1
            child.parent = self

    def is_leave(self):
        return len(self.children) == 0


class Tree:
    def __init__(self, root):
        self.root = root

    def preprocess(self):
        leaves = list(get_leaves(self.root))
        leaves = count_sort(leaves, key=lambda l: l.level)
        leaves.reverse()
        paths = max_path_decompose(leaves, self.root)
        ladder = ladder_decompose(paths)


    def level_ancestor(node, level):
        pass


if __name__ == '__main__':
    root = Node(0)
    a_node = Node(1)
    b_node = Node(1)
    c_node = Node(1)
    d_node = Node(1)
    root.add(a_node, b_node)
    a_node.add(c_node, d_node)

    t = Tree(t)
    t.preprocess()
    print(t.level_ancestor(d_node, 2) is root)
