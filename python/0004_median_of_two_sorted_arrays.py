from typing import List


def _sorted_array(a, a1, a2, a1_idx, a2_idx):
    if a1_idx < len(a1) and a2_idx < len(a2):
        if a1[a1_idx] < a2[a2_idx]:
            a.append(a1[a1_idx])
            a1_idx += 1
        elif a2[a2_idx] < a1[a1_idx]:
            a.append(a2[a2_idx])
            a2_idx += 1
        else:
            a.append(a1[a1_idx])
            a.append(a2[a2_idx])
            a1_idx += 1
            a2_idx += 1
    elif a1_idx < len(a1) and a2_idx >= len(a2):
        a.append(a1[a1_idx])
        a1_idx += 1
    elif a1_idx >= len(a1) and a2_idx < len(a2):
        a.append(a2[a2_idx])
        a2_idx += 1
    else:
        return a

    return _sorted_array(a, a1, a2, a1_idx, a2_idx)


def sorted_array(a1, a2):
    return _sorted_array(list(), a1, a2, 0, 0)


def array_median(a):
    median_idx = len(a) // 2

    if len(a) % 2 == 0:
        return (a[median_idx] + a[median_idx - 1]) / 2
    else:
        return a[median_idx]


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        return array_median(sorted_array(nums1, nums2))
