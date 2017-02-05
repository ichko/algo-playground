#pragma once

#include <map>
using std::map;

namespace Tree {

    template <typename T> struct DisjointSetNode {
        T data;
        DisjointSetNode* parent;
        int depth;

        DisjointSetNode(T& _data, int _depth = 0) : data(_data), parent(this), depth(_depth) { }
    };

    template <typename T> class DisjointSet {

        map<T, DisjointSetNode<T>*> nodesMap;

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
            nodesMap.insert({ data, node });
        }

        void UnionSets(T& first, T& second) {
            auto firstNodeMap = nodesMap.find(first);
            auto secondNodeMap = nodesMap.find(second);

            if (firstNodeMap != nodesMap.end() && secondNodeMap != nodesMap.end()) {
                auto firstNode = firstNodeMap->second;
                auto secondNode = secondNodeMap->second;

                if (firstNode != secondNode) {
                    if (firstNode->depth < secondNode->depth) {
                        firstNode->parent = secondNode;
                        secondNode->depth += firstNode->depth;
                    }
                    else {
                        secondNode->parent = firstNode;
                        firstNode->depth += secondNode->depth;
                    }
                }
            }
        }

        bool IsRoot() {
            return this == parent;
        }

        bool InSameSet(T&& first, T&& second) {
            auto firstNode = Find(first);
            auto secondNode = Find(second);

            return firstNode != nullptr &&
                secondNode != nullptr &&
                firstNode == secondNode;
        }

        DisjointSetNode<T>* Find(T& data) {
            auto nodeMap = nodesMap.find(data);
            if (nodeMap != nodesMap.end()) {
                auto node = nodeMap->second;
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
            for (auto& nodeMap : nodesMap) {
                delete nodeMap.second;
            }
        }

    };

}