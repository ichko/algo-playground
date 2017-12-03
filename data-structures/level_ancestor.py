"""
    Level Ancestor Problem (LA)
"""

class Node:
    def __init__(self, value, children = []):
        self.value = value
        self.children = set(children)

    def add(self, children):
        self.children.update(children)


r = Node(
    0,
    [Node(1, Node(3)), Node(2)]
)

class Tree:
    def __init__(self, root):
        self.root = root

    def preprocess(self):
        pass

    def level_ancestor(node, level):
        pass
