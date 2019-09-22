#!/usr/bin/env python3

# https://leetcode.com/problems/longest-palindrome/

from collections import Counter


def longest_palindrome(s: str) -> int:
    counter = Counter(s)
    single = ""
    multiples = {}

    for c, count in counter.items():
        if count == 1:
            single = c
        if count > 1:
            rest = count % 2
            if not single and rest != 0:
                single = c
            multiples[c] = count - rest

    left = []

    for c, count in multiples.items():
        for _ in range(count // 2):
            left.append(c)

    palindrome = "".join(left) + single + "".join(reversed(left))

    return palindrome


class Solution:
    def longestPalindrome(self, s: str) -> int:
        return len(longest_palindrome(s))
