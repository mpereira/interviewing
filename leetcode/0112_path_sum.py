#!/usr/bin/env python3

# https://leetcode.com/problems/path-sum/

# Runtime: 52 ms, faster than 63.18% of Python3 online submissions for Path Sum.
# Memory Usage: 15.6 MB, less than 5.45% of Python3 online submissions for Path Sum.


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def _traverse_with_sum(node: TreeNode, current_sum: int, check_sum_fn):
    if not node:
        return

    current_sum += node.val

    if not node.left and not node.right:
        check_sum_fn(current_sum)

    _traverse_with_sum(node.left, current_sum, check_sum_fn)
    _traverse_with_sum(node.right, current_sum, check_sum_fn)


def has_path_sum(node: TreeNode, target_sum: int):
    _has_path_sum = False

    def check_sum_fn(path_sum: int):
        nonlocal _has_path_sum
        if path_sum == target_sum:
            _has_path_sum = True

    _traverse_with_sum(node, 0, check_sum_fn)

    return _has_path_sum


class Solution:
    def hasPathSum(self, root: TreeNode, sum: int) -> bool:
        return has_path_sum(root, sum)
