#!/usr/bin/env python3

# https://leetcode.com/problems/climbing-stairs/

# Runtime: 40 ms, faster than 27.45% of Python3 online submissions for Climbing Stairs.
# Memory Usage: 13.9 MB, less than 5.97% of Python3 online submissions for Climbing Stairs.


def ways_to_the_top(n: int, memo: dict) -> int:
    if n in memo:
        return memo[n]

    if n == 0:
        return 1
    elif n == 1:
        return 1
    elif n > 1:
        _ways_to_the_top_1 = ways_to_the_top(n - 1, memo)
        if n - 1 not in memo:
            memo[n - 1] = _ways_to_the_top_1

        _ways_to_the_top_2 = ways_to_the_top(n - 2, memo)
        if n - 2 not in memo:
            memo[n - 2] = _ways_to_the_top_2

        return _ways_to_the_top_1 + _ways_to_the_top_2


class Solution:
    def climbStairs(self, n: int) -> int:
        ways_to_the_top_memo = {}
        return ways_to_the_top(n, ways_to_the_top_memo)
