#pragma once

#include <map>

namespace Trees {

    typedef int unit;

    using std::map;
    using std::ostream;

    #define INDENT ' '
    #define LEAF_MARKER '*'

    template <typename T> class Node {

        T value;
        map<T, Node*> children;
        bool leaf;
        unit level;

    public:
        Node(T _value = T(), bool _leaf = false) : value(_value), leaf(_leaf), level(0) {}

        Node(const Node& node) { copy(node); }

        Node& operator=(const Node& node) {
            if (&node != this) erase();
            copy(node);

            return *this;
        }

        ~Node() { erase(); }


        Node* insert(T& value) {
            auto child = new Node(value);
            children.insert({ value, child });

            return child;
        }

        Node* get_child(T& key) const {
            auto it = children.find(key);
            if (it != children.end()) {
                return it->second;
            }

            return nullptr;
        }

        void erase(unit pos) {
            delete children[pos];
            children[pos] = nullptr;
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

        friend ostream& operator<<(ostream& os, const Node<T>& node) {
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

        void copy(const Node& node) {
            value = node.value;
            leaf = node.leaf;
            for (auto& kv : children) {
                children.insert(kv.first, new Node(kv.second));
            }
        }

        void erase() {
            for (auto& kv : children) {
                delete kv.second;
            }
        }

    };

}