#pragma once

#include <map>

namespace Trees {

    typedef int unit;

    using std::map;
    using std::ostream;

    #define INDENT ' '
    #define LEAF_MARKER '*'

    template <typename T> class TrieNode {

        T value;
        TrieNode* parent;
        map<T, TrieNode*> children;
        bool leaf;
        unit level;

    public:
        TrieNode(T _value = T(), bool _leaf = false) : 
            value(_value), parent(nullptr), leaf(_leaf), level(0) {}

        TrieNode(const TrieNode& node) { copy(node); }

        TrieNode& operator=(const TrieNode& node) {
            if (&node != this) erase();
            copy(node);

            return *this;
        }

        ~TrieNode() { erase(); }


        TrieNode* insert(T& value) {
            auto child = new TrieNode(value);
            children.insert({ value, child });

            return child;
        }

        TrieNode* get_child(T& key) const {
            auto it = children.find(key);
            if (it != children.end()) {
                return it->second;
            }

            return nullptr;
        }

        void erase(T key) {
            auto it = children.find(key);
            if (it != children.end()) {
                delete it->second;
                children.erase(key);
            }
        }

        void set_leaf(bool _leaf = true) {
            leaf = _leaf;
        }

        bool is_leaf() const {
            return leaf;
        }

        void set_level(unit _level) {
            level = _level;
        }

        unit get_level() {
            return level;
        }

        size_t get_num_children() {
            return children.size();
        }

        void set_parent(TrieNode<T>* _parent) {
            parent = _parent;
        }

        TrieNode* get_parent() {
            return parent;
        }

        T& get_value() {
            return value;
        }

        friend ostream& operator<<(ostream& os, const TrieNode<T>& node) {
            node.print(os);
            return os;
        }

    private:
        void print(ostream& os, unit indent = 0) const {
            for (auto i = 0; i < indent; i++) {
                os << INDENT;
            }

            os << (leaf ? LEAF_MARKER : INDENT) << value << endl;

            for (auto& kv : children) {
                kv.second->print(os, indent + 1);
            }
        }

        void copy(const TrieNode& node) {
            value = node.value;
            leaf = node.leaf;
            for (auto& kv : children) {
                children.insert(kv.first, new TrieNode(kv.second));
            }
        }

        void erase() {
            for (auto& kv : children) {
                delete kv.second;
            }
        }

    };

}