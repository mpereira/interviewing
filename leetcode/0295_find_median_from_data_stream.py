from typing import List
from heapq import heappush, heappop

# https://leetcode.com/problems/find-median-from-data-stream/

# Runtime: 248 ms, faster than 27.26% of Python3 online submissions for Find Median from Data Stream.
# Memory Usage: 24.6 MB, less than 6.67% of Python3 online submissions for Find Median from Data Stream.


class MedianFinder:
    def __init__(self):
        # Max heap.
        self.lower_heap = []
        # Min heap.
        self.higher_heap = []

    def balanceHeaps(self):
        lower_heap_len = len(self.lower_heap)
        higher_heap_len = len(self.higher_heap)

        if lower_heap_len - higher_heap_len > 1:
            heappush(self.higher_heap, -1 * heappop(self.lower_heap))
        elif higher_heap_len - lower_heap_len > 1:
            heappush(self.lower_heap, -1 * heappop(self.higher_heap))

    def addNum(self, num: int) -> None:
        lower_heap_max = self.lower_heap and -1 * self.lower_heap[0]
        higher_heap_min = self.higher_heap and self.higher_heap[0]

        if not lower_heap_max or num <= lower_heap_max:
            heappush(self.lower_heap, -1 * num)
        else:
            heappush(self.higher_heap, num)

        self.balanceHeaps()

    def findMedian(self) -> float:
        lower_heap_len = len(self.lower_heap)
        lower_heap_max = self.lower_heap and -1 * self.lower_heap[0]
        higher_heap_len = len(self.higher_heap)
        higher_heap_min = self.higher_heap and self.higher_heap[0]

        if lower_heap_len == higher_heap_len:
            return (lower_heap_max + higher_heap_min) / 2
        elif lower_heap_len > higher_heap_len:
            return lower_heap_max
        elif higher_heap_len > lower_heap_len:
            return higher_heap_min
