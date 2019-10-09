#!/usr/bin/env python3

from collections import deque

# https://leetcode.com/problems/clone-graph/

# Runtime: 36 ms, faster than 99.15% of Python3 online submissions for Clone Graph.
# Memory Usage: 14.6 MB, less than 7.41% of Python3 online submissions for Clone Graph.


class Node:
    def __init__(self, val, neighbors):
        self.val = val
        self.neighbors = neighbors


def bfs(node: "Node", visit_fn=None):
    queue = deque([[node]])
    seen = set([node])
    nodes = [node]

    while queue:
        current_path = queue.popleft()
        current_node = current_path[-1]

        if visit_fn:
            visit_fn(current_node)

        for neighbor in current_node.neighbors:
            if neighbor not in seen:
                seen.add(neighbor)
                nodes.append(neighbor)
                queue.append(current_path + [neighbor])

    return nodes


def clone_graph(node: "Node") -> "Node":
    old_nodes = bfs(node)
    new_nodes = []
    new_to_old = {}
    old_to_new = {}

    for old_node in old_nodes:
        new_node = Node(old_node.val, [])
        new_to_old[new_node] = old_node
        old_to_new[old_node] = new_node
        new_nodes.append(new_node)

    for new_node in new_nodes:
        for old_neighbor in new_to_old[new_node].neighbors:
            new_neighbor = old_to_new[old_neighbor]
            new_node.neighbors.append(new_neighbor)

    return new_nodes[0]


class Solution:
    def cloneGraph(self, node: "Node") -> "Node":
        return clone_graph(node)
