#include <iostream>
#include "trie.cpp"
using namespace std;

int main() {

    Trie<char> trie;

    trie.insert("banana", 6);
    trie.insert("bbnana", 6);
    trie.insert("bananata", 8);
    trie.insert("bananama", 8);

    cout << trie;

}
