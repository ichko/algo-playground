#include <iostream>
#include "includes/trie.cpp"
#include "includes/graph.cpp"
#include "includes/disjoint-set.cpp"

using namespace std;


void KruskalTest() {

}

void DisjointSetTest() {
    int zero = 0;
    int fifty = 50;

    DataStructures::DisjointSet<int> djs;
    djs.MakeSet(fifty);

    for (int i = 0; i < 50; i++) {
        djs.MakeSet(i);
        djs.UnionSets(zero, i);
    }

    cout << djs.InSameSet(5, 10) << djs.InSameSet(0, 49) <<
        djs.InSameSet(0, 50) << djs.InSameSet(10, 51);

}

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
    // TrieTest();
    // DisjointSetTest();
    KruskalTest();
}
