#!/usr/bin/env python3

# https://leetcode.com/problems/power-of-two/


def is_power_of_two(n: int) -> bool:
    while n > 1 and n % 2 == 0:
        n = n // 2

    if n == 1:
        return True

    return False


class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        return is_power_of_two(n)
