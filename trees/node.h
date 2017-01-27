#pragma once

template<typename T>
class Node {

    T value;
    Node* next;
    unit size;

public:
    Node(T& _value, Node* _next = nullptr) : value(_value), next(_next) {}

    Node(const Node& node) { copy(node); }

    Node* operator=(const Node& node) {
        if (node != *this) erase();
        copy(node);

        return this;
    }

    ~Node() { erase(); }

private:
    void copy(const Node& node) {
        value = node.value;
        next = new Node(*this);
    }

    void erase() {
        delete[] next;
    }

};
