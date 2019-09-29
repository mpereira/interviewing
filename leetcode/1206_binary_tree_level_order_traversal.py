#!/usr/bin/env python3

# https://leetcode.com/problems/binary-tree-level-order-traversal/

from typing import List
from collections import deque

# Runtime: 44 ms, faster than 50.99% of Python3 online submissions for Binary
# Tree Level Order Traversal.
# Memory Usage: 14 MB, less than 16.13% of Python3 online submissions for Binary
# Tree Level Order Traversal.


class TreeNode:
    def __init__(self, x: int):
        self.val = x
        self.left = None
        self.right = None


def tree_levels(node: TreeNode):
    paths = deque([[node]])
    levels = []

    while paths:
        path = paths.popleft()
        level = len(path) - 1
        node = path[-1]
        deepest_level_so_far = len(levels) - 1
        if level > deepest_level_so_far:
            levels.append([])
        levels[level].append(node.val)
        if node.left:
            paths.append(path + [node.left])
        if node.right:
            paths.append(path + [node.right])

    return levels


class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root:
            return []
        return tree_levels(root)
