import os
import time
from collections import defaultdict

from tqdm import tqdm


class Huffman:
    class CompositeNode:
        def __init__(self, left, right):
            self.frequency = left.frequency + right.frequency
            self.left = left
            self.right = right

    class LeafNode:
        def __init__(self, letter, frequency):
            self.letter = letter
            self.frequency = frequency

    def __init__(self):
        self.words = []

    def add_words(self, words):
        self.words.extend(words)

    def calc_letter_freq(self):
        self.frequencies = defaultdict(lambda: 0)

        for word in self.words:
            for c in word:
                self.frequencies[c] += 1

    def calc_bigram_freq(self):
        self.frequencies = defaultdict(lambda: 0)

        for word in self.words:
            for a, b in zip(word, word[1:]):
                self.frequencies[(a, b)] += 1

    def build_tree(self):
        import heapq

        self.calc_letter_freq()
        pq = []
        for letter, freq in self.frequencies.items():
            node = Huffman.LeafNode(letter, freq)
            heapq.heappush(pq, (freq, id(node), node))

        while len(pq) > 1:
            left_freq, _, left_node = heapq.heappop(pq)
            right_freq, _, right_node = heapq.heappop(pq)
            node = Huffman.CompositeNode(left_node, right_node)
            heapq.heappush(pq, (left_freq + right_freq, id(node), node))

        _, _, self.tree = heapq.heappop(pq)
        return self.tree

    @staticmethod
    def example_tree():
        huf = Huffman()
        huf.add_words(['AAABAACAADAA', 'BBAACCAADD'])
        huf.build_tree()
        return huf

    def to_graph(self):
        from graphviz import Digraph

        g = Digraph('G', filename='process.gv', format='png')

        g.attr(compound='true')
        g.attr(overlap='false')
        g.attr(rankdir='LR', size='250,250')

        def recur(parent_path, node):
            if isinstance(node, Huffman.LeafNode):
                g.attr('node', shape='doublecircle')
                letter = node.letter
                if type(letter) != str:
                    letter = ''.join(list(letter))

                g.node(parent_path, letter)
                return
            else:
                g.attr('node', shape='circle')
                g.node(parent_path, str(node.frequency))

            l_path = f'{parent_path}l'
            r_path = f'{parent_path}r'

            recur(l_path, node.left)
            recur(r_path, node.right)

            g.edge(parent_path, l_path, label='0')
            g.edge(parent_path, r_path, label='1')

        recur('#', self.tree)
        return g


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
        from graphviz import Digraph

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
        name = name.lower()
        return ''.join(list(filter(lambda x: x.isalpha(), name)))

    all_files = []

    def parse_file(parent_path, parent_name, depth=0):
        if depth > 10:
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
    # huf = Huffman.example_tree()
    # g = huf.to_graph()
    # g.view()

    bar = tqdm(total=4301964)
    tic = time.perf_counter()

    root, all_files = build_fs_tree(bar)

    huf = Huffman()
    huf.add_words(all_files)
    huf.build_tree()
    huf.to_graph().view()

    # fs_trie = Trie.from_words(all_files)
    # fs_trie.to_graph().view()

    toc = time.perf_counter()

    print(f"{toc - tic:0.4f} seconds")

    while True:
        pass
