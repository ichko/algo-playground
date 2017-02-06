#pragma once

#include <map>

namespace DataStructures {

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

        TrieNode(const TrieNode& node) { Copy(node); }

        TrieNode& operator=(const TrieNode& node) {
            if (&node != this) Erase();
            Copy(node);

            return *this;
        }

        ~TrieNode() { Erase(); }


        TrieNode* Insert(T& value) {
            auto child = new TrieNode(value);
            children.insert({ value, child });

            return child;
        }

        TrieNode* GetChild(T& key) const {
            auto it = children.find(key);
            if (it != children.end()) {
                return it->second;
            }

            return nullptr;
        }

        void Erase(T key) {
            auto it = children.find(key);
            if (it != children.end()) {
                delete it->second;
                children.erase(key);
            }
        }

        void SetLeaf(bool _leaf = true) {
            leaf = _leaf;
        }

        bool IsLeaf() const {
            return leaf;
        }

        void SetLevel(unit _level) {
            level = _level;
        }

        unit GetLevel() {
            return level;
        }

        size_t GetChildrenSize() {
            return children.size();
        }

        void SetParent(TrieNode<T>* _parent) {
            parent = _parent;
        }

        TrieNode* GetParent() {
            return parent;
        }

        T& GetValue() {
            return value;
        }

        friend ostream& operator<<(ostream& os, const TrieNode<T>& node) {
            node.Print(os);
            return os;
        }

    private:
        void Print(ostream& os, unit indent = 0) const {
            for (auto i = 0; i < indent; i++) {
                os << INDENT;
            }

            os << (leaf ? LEAF_MARKER : INDENT) << value << endl;

            for (auto& kv : children) {
                kv.second->Print(os, indent + 1);
            }
        }

        void Copy(const TrieNode& node) {
            value = node.value;
            leaf = node.leaf;
            for (auto& kv : children) {
                children.insert(kv.first, new TrieNode(kv.second));
            }
        }

        void Erase() {
            for (auto& kv : children) {
                delete kv.second;
            }
        }

    };

}