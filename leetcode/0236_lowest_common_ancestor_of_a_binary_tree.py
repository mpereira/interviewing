#!/usr/bin/env python3

from typing import List
from collections import deque

# https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/

# Runtime: 540 ms, faster than 5.06% of Python3 online submissions for Lowest Common Ancestor of a Binary Tree.
# Memory Usage: 17.9 MB, less than 91.67% of Python3 online submissions for Lowest Common Ancestor of a Binary Tree.


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def bfs(root: TreeNode, visit_fn=None, stop_search_fn=None):
    paths = deque([[root]])
    seen = set([root])

    while paths and not stop_search_fn():
        path = paths.pop()
        node = path[-1]

        if visit_fn:
            visit_fn(node, path)

        for child in [node.left, node.right]:
            if child and child not in seen:
                paths.appendleft(path + [child])
                seen.add(child)


def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode):
    p_path = None
    q_path = None

    def get_node_paths(node, path):
        nonlocal p_path
        nonlocal q_path
        if node == p:
            p_path = path
        if node == q:
            q_path = path

    def node_paths_found():
        nonlocal p_path
        nonlocal q_path
        return p_path and q_path

    # TODO: possible improvement is to use DFS?
    bfs(root, visit_fn=get_node_paths, stop_search_fn=node_paths_found)

    p_node_idx = 0
    p_node = p_path[p_node_idx]
    q_node_idx = 0
    q_node = q_path[q_node_idx]

    while True:
        p_node_next_idx = p_node_idx + 1
        q_node_next_idx = q_node_idx + 1

        if p_node_next_idx >= len(p_path) or q_node_next_idx >= len(q_path):
            break

        if p_path[p_node_next_idx] != q_path[q_node_next_idx]:
            break

        p_node_idx += 1
        q_node_idx += 1
        p_node = p_path[p_node_idx]
        q_node = q_path[q_node_idx]

    return p_node


class Solution:
    def lowestCommonAncestor(
        self, root: TreeNode, p: TreeNode, q: TreeNode
    ) -> "TreeNode":
        return lowest_common_ancestor(root, p, q)
