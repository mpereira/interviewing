#!/usr/bin/env python3

# https://leetcode.com/problems/single-number/

from typing import List
from collections import defaultdict


def single_number(xs: List[int]) -> int:
    x_occurrence_counts = defaultdict(int)

    for x in xs:
        if x_occurrence_counts[x] > 0:
            del x_occurrence_counts[x]
            continue

        x_occurrence_counts[x] += 1

    return next(iter(x_occurrence_counts.keys()))


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        return single_number(nums)
