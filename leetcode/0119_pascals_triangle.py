#!/usr/bin/env python3

# https://leetcode.com/problems/pascals-triangle

from typing import List


def build_pascal_triangle(number_of_rows: int) -> List[List[int]]:
    if number_of_rows == 0:
        return []

    rows = [[1]] + [[] for _ in range(number_of_rows - 1)]

    for row in range(1, number_of_rows):
        number_of_columns = row + 1
        previous_row = rows[row - 1]
        for column in range(number_of_columns):
            value = 0

            if column > 0:
                value += previous_row[column - 1]

            if column < number_of_columns - 1:
                value += previous_row[column]

            rows[row].append(value)

    return rows


class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        return build_pascal_triangle(numRows)
