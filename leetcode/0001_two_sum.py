from typing import List


def two_sum(numbers, target):
    memo = {}

    for idx, number in enumerate(numbers):
        complement = target - number
        if complement in memo:
            return memo[complement].pop(), idx

        if number in memo:
            memo[number].append(idx)
        else:
            memo[number] = [idx]


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        return list(two_sum(nums, target))
