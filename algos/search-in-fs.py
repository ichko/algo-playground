import os
import time
from tqdm import tqdm

from graphviz import Digraph


class Trie:
    class Node:
        def __init__(self, value):
            self.value = value
            self.end_node = False
            self.children = {}

        def add_child(self, node):
            self.children[node.value] = node

    def __init__(self):
        self.root = Trie.Node(value='#')

    def add_word(self, word):
        def recur(node, index):
            if index >= len(word):
                node.end_node = True
                return

            letter = word[index]
            if letter not in node.children:
                new_node = Trie.Node(letter)
                node.add_child(new_node)

            recur(node.children[letter], index + 1)

        recur(self.root, 0)

    def to_graph(self):
        g = Digraph('G', filename='process.gv', format='png')

        g.attr(compound='true')
        g.attr(overlap='false')
        g.attr(rankdir='TB', size='250,250')

        prefixes = set()

        def recur(parent_path, node):
            parent_name = node.value
            if parent_path not in prefixes:
                if node.end_node:
                    g.attr('node', shape='doublecircle')
                else:
                    g.attr('node', shape='circle')
                g.node(parent_path, parent_name)

            for child_name, child in node.children.items():
                child_path = f'{parent_path}{child_name}'
                recur(child_path, child)
                g.edge(parent_path, child_path, label='')

        recur('', self.root)
        return g

    @staticmethod
    def trie_example():
        trie = Trie()
        trie.add_word('ad')
        trie.add_word('acd')
        trie.add_word('acdc')
        trie.add_word('abd')
        trie.add_word('abcd')
        trie.add_word('abbcd')
        return trie

    @staticmethod
    def from_words(words):
        trie = Trie()
        for word in words:
            trie.add_word(word)
        return trie


def build_fs_tree(bar):
    def filter_name(name):
        return ''.join(list(filter(lambda x: x.isalnum(), name)))

    all_files = []

    def parse_file(parent_path, parent_name, depth=0):
        if depth > 2:
            return

        bar.update(1)
        parent_name = filter_name(parent_name)
        all_files.append(parent_name)

        if os.path.isdir(parent_path) and not os.path.islink(parent_path):
            try:
                children_names = os.listdir(parent_path)

                children_paths = [
                    os.path.join(parent_path, c) for c in children_names
                ]

                children = []
                for child_path, child_name in zip(children_paths,
                                                  children_names):
                    child = parse_file(child_path, child_name, depth=depth + 1)

                    children.append(child)
            except PermissionError:
                return {parent_name: ['no permissions']}
            except OSError:
                return {parent_name: ['os error']}

            return {parent_name: children}
        else:
            return parent_name

    root = parse_file('/', 'root')
    return root, all_files


if __name__ == '__main__':
    bar = tqdm(total=4301964)
    tic = time.perf_counter()

    root, all_files = build_fs_tree(bar)
    fs_trie = Trie.from_words(all_files)
    fs_trie.to_graph().view()

    toc = time.perf_counter()

    print(f"{toc - tic:0.4f} seconds")

    while True:
        pass
