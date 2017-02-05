#include <iostream>
#include "includes/trie.cpp"
#include "includes/disjoint-set.cpp"
using namespace std;

int main() {



}


void trieTest() {
    Trees::Trie<char> trie;

    trie.insert("banana", 6);
    trie.insert("bbnana", 6);
    trie.insert("bananata", 8);
    trie.insert("bananama", 8);
    trie.erase("banana", 6);
    trie.erase("bananama", 8);

    cout << trie.contains("banana", 6) << endl;
    cout << trie.contains("banaza", 6) << endl;
    cout << trie.contains_prefix("ban", 3) << endl;

    cout << trie;
}