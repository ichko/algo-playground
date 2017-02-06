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
                auto from_node = RetrieveVertex(from);
                auto to_node = RetrieveVertex(to);

                auto new_edge = new Edge(from_node, to_node, weight);
                edges.insert({ make_pair(from, to), new_edge })
            }
        }

        vector<Edge*> GetMinimalSpanningTree() {
            vector<Edge*> result;
            DisjointSet<Vertex*> djs;

            sort(edges.begin(), edges.end());

            for (auto& node_map : nodes) {
                djs.MakeSet(node_map.second);
            }

            for (auto& edge_map : edges) {
                auto edge = edge_map.second;
                if (!djs.InSameSet(edge->from, edge->to)) {
                    result.push_back(edge);
                    djs.UnionSets(edge->from, edge->to);
                }
            }

            return result;
        }

    private:
        Vertex* RetrieveVertex(T& value) {
            auto node_map = nodes.find(value);

            if (node_map != nodes.end()) {
                return node_map.second;
            }

            auto new_node = new Vertex(value);
            nodes.insert({ value, new_node });

            return new_node;
        }

    };

}