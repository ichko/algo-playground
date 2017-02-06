#include <iostream>
#include "includes/trie.cpp"
#include "includes/graph.cpp"
#include "includes/disjoint-set.cpp"

using namespace std;


void KruskalTest() {
    DataStructures::Graph<int> graph;
    graph.InsertEdge(1, 5, 7);
    graph.InsertEdge(2, 1, 4);
    graph.InsertEdge(2, 4, 3);
    graph.InsertEdge(2, 3, 2);
    graph.InsertEdge(3, 4, 1);
    graph.InsertEdge(5, 2, 1);

    auto tree = graph.GetMinimalSpanningTree();
    for (auto& edge : tree) {
        cout << edge->from->value << " - " << edge->to->value << endl;
    }
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
    DataStructures::Trie<char> trie;

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
