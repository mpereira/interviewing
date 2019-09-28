#!/usr/bin/env python3

from typing import List


def _binary_search(xs: List[int], n: int, left: int, right: int) -> int:
    if left > right:
        return None

    mid = left + ((right - left) // 2)

    if xs[mid] == n:
        return mid

    if n > xs[mid]:
        return _binary_search(xs, n, mid + 1, right)

    if n < xs[mid]:
        return _binary_search(xs, n, left, mid - 1)


def binary_search(xs: List[int], n: int) -> int:
    if not xs or n < xs[0] or n > xs[-1]:
        return None

    return _binary_search(xs, n, 0, len(xs) - 1)
