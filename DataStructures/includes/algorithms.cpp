#pragma once

#include <vector>
#include "graph.cpp"
#include "disjoint-set.cpp"

using std::vector;

namespace DSAA {

    template <typename T> vector<Edge*> GetMinimalSpanningTree(Graph<T>& graph) {
        vector<Edge*> result;
        vector<Edge*> sorted_edges;
        DisjointSet<Vertex*> djs;

        for (auto& edge_map : *graph.GetEdges()) {
            sorted_edges.push_back(edge_map.second);
        }

        sort(sorted_edges.begin(), sorted_edges.end(),
            [](const Edge* left, const Edge* right) -> int
        {
            return left->weight < right->weight;
        });

        for (auto& node_map : *graph.GetVertecies()) {
            djs.MakeSet(node_map.second);
        }

        for (auto& edge : sorted_edges) {
            if (!djs.InSameSet(edge->from, edge->to)) {
                result.push_back(edge);
                djs.UnionSets(edge->from, edge->to);
            }
        }

        return result;
    };

}
