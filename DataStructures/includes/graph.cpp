#pragma once

#include <algorithm>
#include <vector>
#include <map>
#include "disjoint-set.cpp"

using std::vector;
using std::map;
using std::pair;
using std::make_pair;
using std::sort;

#define Vertex GraphNode<T>
#define Edge GraphEdge<T>


namespace DataStructures {

    template <typename T> struct GraphNode {

        T value;

        GraphNode(T& _value) : value(_value) { }

    };

    template <typename T> struct GraphEdge {

        Vertex* from;
        Vertex* to;
        int weight;

        GraphEdge(Vertex* _from, Vertex* _to, int _weight = 0) :
            from(_from), to(_to), weight(_weight) { }

        bool operator<(const Edge& edge) const {
            return weight < edge.weight;
        }

    };



    template <typename T> class Graph {

        map<T, Vertex*> nodes;
        map<pair<T, T>, Edge*> edges;

    public:
        void InsertNode(T& value) {
            auto node = new Vertex(value);
            nodes.insert({ value, node })
        }

        void InsertEdge(T& from, T& to, int weight = 0) {
            auto edge = edges.find({ from, to });
            if (edge == edges.end()) {
                auto new_edge = new Edge(from, to, weight);
                edges.insert({ make_pair(from, to), new_edge })
            }
        }

        DisjointSet<Edge*> GetMinimalSpanningTree() {
            DisjointSet<Vertex*> result;
            sort(edges.begin(), edges.end());

            for (auto& node_map : nodes) {
                result.MakeSet(node_map.second);
            }

            for (auto& edge_map : edges) {
                auto edge = edge_map.second;
                if (!result.InSameSet(edge->from, edge->to)) {
                    result.UnionSets(edge->from, edge->to);
                }
            }

            return result;
        }

    };

}