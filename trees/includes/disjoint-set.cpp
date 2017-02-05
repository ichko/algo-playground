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

        map<T, DisjointSetNode<T>* > nodesMap;

    public:
        DisjointSet(const DisjointSet& djs) { copy(djs); }

        DisjointSet& operator=(const DisjointSet& djs) {
            if (&djs != this) {
                erase();
                copy(djs);
            }

            return *this;
        }

        ~DisjointSet() { erase(); }


        void makeSet(T& data) {
            auto node = new DisjointSetNode(data);
            nodesMap.insert(data, node);
        }

        void unionSets(T& first, T& second) {
            auto firstNodeMap = nodesMap.find(first);
            auto secondNodeMap = nodesMap.find(second);

            if (firstNodeMap != nodesMap.end() && secondNodeMap != nodesMap.end()) {
                auto firstNode = firstNodeMap->second;
                auto secondNode = secondNodeMap->second;

                if (firstNode != secondNode) {
                    if (firstNode->depth < secondNode->depth) {
                        firstNode->parent = secondNode;
                        secondNode += firstNode->depth;
                    }
                    else {
                        secondNode->parent = firstNode;
                        firstNode += secondNode->depth;
                    }
                }
            }
        }

        bool isRoot() {
            return this == parent;
        }

        bool inSameSet(T&& left, T&& right) {
            auto firstNodeMap = nodesMap.find(first);
            auto secondNodeMap = nodesMap.find(second);

            return firstNodeMap != nodesMap.end() &&
                secondNodeMap != nodesMap.end() &&
                firstNodeMap->second == secondNodeMap->second;
        }

        DisjointSetNode<T>* find(T& data) {
            auto nodeMap = nodesMap.find(data);
            if (node != nodesMap.end()) {
                auto node = nodeMap->second;
                while (node != node->parent) {
                    node.parent = find(node->parent->data);
                }

                return node;
            }

            return nullptr;
        }

    private:
        void copy(const DisjointSet& djs) {
            data = djs.data;
            depth = djs.depth;
            parent = new DisjointSet(djs.parent);
        }

        void erase() {
            for (auto& nodeMap : nodesMap) {
                delete nodeMap->second;
            }
        }

    };

}