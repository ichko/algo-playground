#pragma once

#include "node.cpp"

namespace Trees {

    typedef int unit;
    #define ROOT_VALUE '#'

    template <typename T> class Trie {

        TrieNode<T> root;

    public:
        Trie() : root(ROOT_VALUE) {}

        void insert(T* values, unit size) {
            auto parent = find(&root, values, size);

            if (parent != nullptr) {
                for (auto i = parent->get_level(); i < size; i++) {
                    auto old_parent = parent;
                    parent = parent->insert(values[i]);
                    parent->set_level(old_parent->get_level() + 1);
                    parent->set_parent(old_parent);
                }
                parent->set_leaf(true);
            }
        }

        bool contains(T* values, unit size) {
            auto node = find(&root, values, size);
            return node != nullptr && node->is_leaf() && node->get_level() == size;
        }

        bool contains_prefix(T* values, unit size) {
            auto node = find(&root, values, size);
            return node != nullptr && node->get_level() == size;
        }

        void erase(T* values, unit size) {
            auto node = find(&root, values, size);
            if (node != nullptr && node->is_leaf() && node->get_level() == size && size > 0) {
                node->set_leaf(false);
                if (node->get_num_children() > 0) return;

                auto parent = node->get_parent();
                auto old_parent = parent;
                while (parent != nullptr && !(parent->get_num_children() > 1)) {
                    old_parent = parent;
                    parent = parent->get_parent();
                }

                if (parent != nullptr) {
                    parent->erase(old_parent->get_value());
                }
            };
        }

        friend ostream& operator<<(ostream& os, const Trie<T>& trie) {
            os << trie.root;
            return os;
        }

    private:
        TrieNode<T>* find(TrieNode<T>* parent, T* values, unit size) {
            auto old_parent = parent;
            for (auto i = 0; i < size; i++) {
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
