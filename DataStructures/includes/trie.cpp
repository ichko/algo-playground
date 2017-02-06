#pragma once

#include "trie-node.cpp"

namespace DataStructures {

    typedef int unit;
    #define ROOT_VALUE '#'

    template <typename T> class Trie {

        TrieNode<T> root;

    public:
        Trie() : root(ROOT_VALUE) {}

        void Insert(T* values, unit size) {
            auto parent = Find(&root, values, size);

            if (parent != nullptr) {
                for (auto i = parent->GetLevel(); i < size; i++) {
                    auto old_parent = parent;
                    parent = parent->Insert(values[i]);
                    parent->SetLevel(old_parent->GetLevel() + 1);
                    parent->SetParent(old_parent);
                }
                parent->SetLeaf(true);
            }
        }

        bool Contains(T* values, unit size) {
            auto node = Find(&root, values, size);
            return node != nullptr && node->IsLeaf() && node->GetLevel() == size;
        }

        bool ContainsPrefix(T* values, unit size) {
            auto node = Find(&root, values, size);
            return node != nullptr && node->GetLevel() == size;
        }

        void Erase(T* values, unit size) {
            auto node = Find(&root, values, size);
            if (node != nullptr && node->IsLeaf() && node->GetLevel() == size && size > 0) {
                node->SetLeaf(false);
                if (node->GetChildrenSize() > 0) return;

                auto parent = node->GetParent();
                auto old_parent = parent;
                while (parent != nullptr && !(parent->GetChildrenSize() > 1)) {
                    old_parent = parent;
                    parent = parent->GetParent();
                }

                if (parent != nullptr) {
                    parent->Erase(old_parent->GetValue());
                }
            };
        }

        friend ostream& operator<<(ostream& os, const Trie<T>& trie) {
            os << trie.root;
            return os;
        }

    private:
        TrieNode<T>* Find(TrieNode<T>* parent, T* values, unit size) {
            auto old_parent = parent;
            for (auto i = 0; i < size; i++) {
                if (parent != nullptr) {
                    old_parent = parent;
                    parent = parent->GetChild(values[i]);
                }
                else {
                    return old_parent;
                }
            }

            return parent;
        }

    };
}
