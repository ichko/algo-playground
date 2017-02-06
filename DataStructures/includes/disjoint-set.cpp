#pragma once

#include <map>
using std::map;

namespace DSAA {

    template <typename T> struct DisjointSetNode {
        T data;
        DisjointSetNode* parent;
        int depth;

        DisjointSetNode(T& _data, int _depth = 0) : data(_data), parent(this), depth(_depth) { }
    };

    template <typename T> class DisjointSet {

        map<T, DisjointSetNode<T>*> nodes_map;

    public:
        DisjointSet() { }

        DisjointSet(const DisjointSet& djs) { Copy(djs); }

        DisjointSet& operator=(const DisjointSet& djs) {
            if (&djs != this) {
                Erase();
                Copy(djs);
            }

            return *this;
        }

        ~DisjointSet() { Erase(); }

        void MakeSet(T& data) {
            auto node = new DisjointSetNode<T>(data);
            nodes_map.insert({ data, node });
        }

        void UnionSets(T& first, T& second) {
            auto first_node_map = nodes_map.find(first);
            auto second_node_map = nodes_map.find(second);

            if (first_node_map != nodes_map.end() && second_node_map != nodes_map.end()) {
                auto first_node = first_node_map->second;
                auto second_node = second_node_map->second;

                if (first_node != second_node) {
                    if (first_node->depth < second_node->depth) {
                        first_node->parent = second_node;
                        second_node->depth += first_node->depth;
                    }
                    else {
                        second_node->parent = first_node;
                        first_node->depth += second_node->depth;
                    }
                }
            }
        }

        bool IsRoot() {
            return this == parent;
        }

        bool InSameSet(T first, T second) {
            auto first_node = Find(first);
            auto second_node = Find(second);

            return first_node != nullptr &&
                second_node != nullptr &&
                first_node == second_node;
        }

        DisjointSetNode<T>* Find(T& data) {
            auto node_map = nodes_map.find(data);
            if (node_map != nodes_map.end()) {
                auto node = node_map->second;
                if (node != node->parent) {
                    node->parent = Find(node->parent->data);
                }

                return node->parent;
            }

            return nullptr;
        }

    private:
        void Copy(const DisjointSet& djs) {
            data = djs.data;
            depth = djs.depth;
            parent = new DisjointSet(djs.parent);
        }

        void Erase() {
            for (auto& node_map : nodes_map) {
                delete node_map.second;
            }
        }

    };

}