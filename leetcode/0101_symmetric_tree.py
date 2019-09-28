#!/usr/bin/env python3

# https://leetcode.com/problems/symmetric-tree/

from typing import List


def xor(a, b) -> bool:
    return bool(a) ^ bool(b)


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def recursive_are_trees_symmetric(t1: TreeNode, t2: TreeNode) -> bool:
    if not t1 and not t2:
        return True

    if xor(t1, t2):
        return False

    if t1.val == t2.val:
        return recursive_are_trees_symmetric(
            t1.left, t2.right
        ) and recursive_are_trees_symmetric(t1.right, t2.left)

    return False


def iterative_are_trees_symmetric(t1: TreeNode, t2: TreeNode) -> bool:
    t1_path = tree_in_order_path(t1)
    t1_path_len = len(t1_path)
    t2_path = tree_in_order_path(t2)
    t2_path_len = len(t2_path)

    if t1_path_len != t2_path_len:
        return False

    t1_idx = 0
    t2_idx = t2_path_len - 1

    while t2_idx >= 0 and t1_idx < t1_path_len:
        t1_node = t1_path[t1_idx]
        t2_node = t2_path[t2_idx]

        if t1_node.val != t2_node.val:
            return False

        if t1_node.left and not t2_node.right:
            return False

        if t1_node.right and not t2_node.left:
            return False

        if (
            t1_node.right
            and t2_node.left
            and t1_node.right.val != t2_node.left.val
        ):
            return False

        if (
            t1_node.left
            and t2_node.right
            and t1_node.left.val != t2_node.right.val
        ):
            return False

        t1_idx += 1
        t2_idx -= 1

    return True


def tree_in_order_path(tree: TreeNode) -> List[TreeNode]:
    path = []
    stack = []
    p = tree

    while True:
        if p:
            stack.append(p)
            p = p.left
        else:
            if len(stack) == 0:
                break

            node = stack.pop()
            path.append(node)
            p = node.right

    return path


def recursive_is_tree_symmetric(tree: TreeNode) -> bool:
    if not tree:
        return True

    return recursive_are_trees_symmetric(tree.left, tree.right)


def iterative_is_tree_symmetric(tree: TreeNode) -> bool:
    if not tree:
        return True

    return iterative_are_trees_symmetric(tree.left, tree.right)


class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        # return recursive_is_tree_symmetric(root)
        return iterative_is_tree_symmetric(root)
