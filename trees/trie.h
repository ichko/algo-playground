#pragma once

#include "node.h"

typedef int unit;

template<typename T>
class Trie {

    Node<T>* root;
    unit size;

public:
    Trie() : root(nullptr), size(0) {}

    void insert(T* values, unit size) {
        for (unit i = 0; i < size; i++) {

        }
    }

};
