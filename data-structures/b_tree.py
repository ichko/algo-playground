"""
10.2 B Trees and B+ Trees. How they are useful in Databases
- https://www.youtube.com/watch?v=aZjYr87r1b8


M-way search tree
 - Generalization of BSTs
 - Like BST, but with multiple children
"""


class MWayNode:
    def __init__(self):
        self.values = []
        self.children = []

    def insert(self, value):
        self.values.append(value)

    def insert_sorted(self, value):
        if len(self.values) == 0:
            self.values.append(value)

        self.values.append(None)
        for i in range(len(value) - 2, -1, -1):
            v = self.values[i]
            if v <= value:
                self.values[i + 1] = value
                break
            self.values[i + 1] = self.values[i]

    def add_child(self, child):
        self.children.append(child)


def BTree:
    def __init__(self, ):
        pass
