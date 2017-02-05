#include <iostream>
#include "includes/trie.cpp"
#include "includes/disjoint-set.cpp"
using namespace std;


void TrieTest() {
    Trees::Trie<char> trie;

    trie.Insert("banana", 6);
    trie.Insert("bbnana", 6);
    trie.Insert("bananata", 8);
    trie.Insert("bananama", 8);
    trie.Erase("banana", 6);
    trie.Erase("bananama", 8);

    cout << trie.Contains("banana", 6) << endl;
    cout << trie.Contains("banaza", 6) << endl;
    cout << trie.ContainsPrefix("ban", 3) << endl;

    cout << trie;
}


int main() {
    TrieTest();
}
