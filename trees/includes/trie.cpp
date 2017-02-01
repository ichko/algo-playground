#pragma once

#include "node.cpp"

namespace Trees {

    typedef int unit;
    #define ROOT_VALUE '#'

    template <typename T> class Trie {

        Node<T> root;

    public:
        Trie() : root(ROOT_VALUE) {}

        void insert(T* values, unit size) {
            Node<T>* parent = find(&root, values, size);

            if (parent != nullptr) {
                for (unit i = parent->get_level(); i < size; i++) {
                    auto old_parent = parent;
                    parent = parent->insert(values[i]);
                    parent->set_level(old_parent->get_level() + 1);
                }
                parent->set_leaf(true);
            }
        }

        bool contains(T* values, unit size) {
            Node<T>* parent = find(&root, values, size);
            return parent != nullptr && parent->is_leaf() && parent->get_level() == size;
        }

        bool contains_prefix(T* values, unit size) {
            Node<T>* parent = find(&root, values, size);
            return parent != nullptr && parent->get_level() == size;
        }

        friend ostream& operator<<(ostream& os, const Trie<T>& trie) {
            os << trie.root;
            return os;
        }

    private:
        Node<T>* find(Node<T>* parent, T* values, unit size) {
            auto old_parent = parent;
            for (unit i = 0; i < size; i++) {
                if (parent != nullptr) {
                    old_parent = parent;
                    parent = parent->get_child(values[i]);
                }
                else {
                    return old_parent;
                }
            }

            return parent;
        }

    };
}
