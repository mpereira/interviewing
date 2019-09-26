#!/usr/bin/env python3

# https://leetcode.com/problems/maximum-subarray/

from typing import List


def maximum_sub_array(xs: List[int]) -> int:
    maximum_ending_at = [None] * len(xs)
    maximum_ending_at[0] = xs[0]

    for i in range(1, len(xs)):
        previous_sum = maximum_ending_at[i - 1]
        current_sum = previous_sum + xs[i]
        if current_sum > xs[i]:
            maximum_ending_at[i] = current_sum
        else:
            maximum_ending_at[i] = xs[i]

    return max(maximum_ending_at)


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        return maximum_sub_array(nums)
