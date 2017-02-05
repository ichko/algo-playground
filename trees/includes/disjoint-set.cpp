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

        ~DisjointSet() { erase(); }

    private:
        void erase() {
            for (auto& nodeMap : nodesMap) {
                delete nodeMap->second;
            }
        }

    };

}