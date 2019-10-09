#!/usr/bin/env python3

from typing import List

# https://leetcode.com/problems/letter-combinations-of-a-phone-number/

# Runtime: 20 ms, faster than 99.99% of Python3 online submissions for Letter Combinations of a Phone Number.
# Memory Usage: 13.9 MB, less than 5.88% of Python3 online submissions for Letter Combinations of a Phone Number.


class Trie:
    def __init__(self, s: str):
        self.s = s
        self.children = []

    def add_child(self, child: "Trie"):
        self.children.append(child)

    def add_child_with_s(self, s: str):
        self.add_child(Trie(s))


digit_to_chars = {
    "1": "",
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}


def _build_digits_trie(trie: Trie, digits: str):
    if not digits:
        return trie

    current_digit = digits[0]
    next_digits = digits[1:]

    chars = digit_to_chars[current_digit]

    if not chars:
        _build_digits_trie(trie, next_digits)

    for c in chars:
        trie.add_child_with_s(c)

    for c in trie.children:
        _build_digits_trie(c, next_digits)

    return trie


def build_digits_trie(digits: str):
    return _build_digits_trie(Trie(""), digits)


def traverse_with_path(trie: Trie, path: str, combinations: List[str]):
    if not trie:
        return

    current_path = f"{path}{trie.s}"
    if not trie.children:
        combinations.append(current_path)

    for child in trie.children:
        traverse_with_path(child, current_path, combinations)


def traverse(trie: Trie):
    combinations = []
    if not trie.children:
        return combinations
    traverse_with_path(trie, trie.s, combinations)
    return combinations


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        return traverse(build_digits_trie(digits))
