#!/usr/bin/env python3

# https://leetcode.com/problems/first-unique-character-in-a-from/

from collections import defaultdict


def first_unique_character_offset(s: str) -> int:
    c_occurrence_counts = defaultdict(int)
    for occurrence_count, c in enumerate(s):
        c_occurrence_counts[c] += 1

    for offset, c in enumerate(s):
        if c_occurrence_counts[c] == 1:
            return offset

    return -1


class Solution:
    def firstUniqChar(self, s: str) -> int:
        return first_unique_character_offset(s)
