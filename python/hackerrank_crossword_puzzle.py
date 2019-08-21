#!/bin/python3

from pprint import pprint

import json
import math
import os
import random
import re
import sys


def make_hash_key(obj):
    if isinstance(obj, set):
        obj = list(obj)

    return json.dumps(obj)


def parse_hash_key(key):
    return json.loads(key)


def parse_crossword_words(crossword_input):
    return crossword_input[len(crossword_input) - 1].split(";")


def parse_crossword(crossword_input):
    return crossword_input[0 : len(crossword_input) - 1]


# concepts:
#
# 1. cell
# 2. range
# 3. range intersection
# 4. solution
#
# algorithm:
#
# 1. get 'words_by_length', with their lengths
#
#    {4 ["ABBA" "BREW"]
#     5 ["COLIN" "RANGE"]}
#
# 2. get 'range_lenghts'
#
#    {[[0 0] [0 3]] 4
#     [[0 1] [4 1]] 5}
#
# 3. get 'ranges_intersections'. there could be more than two ranges for
#    a given intersection
#
#    {[[[0 0] [0 3]]
#      [[0 1] [4 1]]] [0 1]}
#
# 4. create 'possible_range_words' by matching 'words_by_length' with
#    'range_lenghts'
#
#    {[[0 0] [0 3]] ["ABBA" "BREW"]
#     [[0 1] [4 1]] ["COLIN" "RANGE"]}
#
# 5. for each 'ranges_intersections', check which candidates match the
#    intersecting character by getting 'range_lenghts' and
#    'words_by_length', creating 'intersecting_ranges_solutions'
#
#    {[[[0 0] [0 3]] [[0 1] [4 1]]] [["BREW" "RANGE"]]}
#
# 6. some 'intersecting_ranges_solutions' will only have 1 solution. fill those
#    and remove them from the set of 'pending_words'
#
# 7. for the remaining 'intersecting_ranges_solutions', try all possible
#    combinations
#
# 6. 'solution'
#
#    {[[0 0] [0 3]] "BREW"
#     [[0 1] [4 1]] "RANGE"}


BLANK_CELL = "-"


def make_2d_matrix(rows, columns, value):
    return [[value for i in range(rows)] for j in range(columns)]


def step(crossword, pending_words):
    pass


def is_blank_cell(crossword, cell):
    return crossword[cell[0]][cell[1]] == BLANK_CELL


def cell_to_the_right(matrix, cell):
    _cell_to_the_right = [cell[0], cell[1] + 1]
    if _cell_to_the_right[0] < len(matrix) and _cell_to_the_right[1] < len(matrix[0]):
        return _cell_to_the_right


def cell_to_the_left(matrix, cell):
    _cell_to_the_left = [cell[0], cell[1] - 1]
    if _cell_to_the_left[0] < len(matrix) and _cell_to_the_left[1] < len(matrix[0]):
        return _cell_to_the_left


def cell_below(matrix, cell):
    _cell_below = [cell[0] + 1, cell[1]]
    if _cell_below[0] < len(matrix) and _cell_below[1] < len(matrix[0]):
        return _cell_below


def cell_above(matrix, cell):
    _cell_above = [cell[0] - 1, cell[1]]
    if _cell_above[0] < len(matrix) and _cell_above[1] < len(matrix[0]):
        return _cell_above


def get_cell(matrix, cell):
    if cell and cell[0] < len(matrix) and cell[1] < len(matrix[0]):
        return matrix[cell[0]][cell[1]]


def move_cell_down(cell):
    cell[0] += 1


def move_cell_to_the_right(cell):
    cell[1] += 1


def range_length(_range):
    start = _range[0]
    end = _range[1]
    row_distance = abs(start[0] - end[0])
    column_distance = abs(start[1] - end[1])
    if row_distance > 0:
        row_distance += 1
    if column_distance > 0:
        column_distance += 1
    return row_distance + column_distance


def fill_range(matrix, _range, value):
    start = _range[0]
    end = _range[1]
    for i in range(start[0], end[0] + 1):
        for j in range(start[1], end[1] + 1):
            if matrix[i][j]:
                matrix[i][j].append(value)
            else:
                matrix[i][j] = [value]
    return matrix


def find_ranges_starting_at(crossword, cells_ranges, starting_cell):
    if not is_blank_cell(crossword, starting_cell):
        return set()

    _cell_below = cell_below(crossword, starting_cell)
    _cell_to_the_right = cell_to_the_right(crossword, starting_cell)
    range_below = None
    range_to_the_right = None
    number_of_rows = len(crossword)
    number_of_columns = len(crossword[0])

    # TODO: refactor into function that can be reused in the code block below.
    if (
        _cell_below
        and not get_cell(cells_ranges, _cell_below)
        and is_blank_cell(crossword, _cell_below)
    ):
        current_cell = _cell_below.copy()
        while current_cell[0] < number_of_rows:
            ending_cell = None

            if current_cell[0] == number_of_rows - 1:
                if is_blank_cell(crossword, current_cell):
                    ending_cell = current_cell
            elif not is_blank_cell(crossword, current_cell):
                _cell_above = cell_above(crossword, current_cell)
                if current_cell != _cell_above:
                    ending_cell = cell_above(crossword, current_cell)

            if ending_cell:
                range_below = [starting_cell, ending_cell]
                break

            move_cell_down(current_cell)

    # TODO: refactor into function that can be reused in the code block above.
    if (
        _cell_to_the_right
        and not get_cell(cells_ranges, _cell_to_the_right)
        and is_blank_cell(crossword, _cell_to_the_right)
    ):
        current_cell = _cell_to_the_right.copy()
        while current_cell[1] < number_of_columns:
            ending_cell = None

            if current_cell[1] == number_of_columns - 1:
                if is_blank_cell(crossword, current_cell):
                    ending_cell = current_cell
            elif not is_blank_cell(crossword, current_cell):
                _cell_to_the_left = cell_to_the_left(crossword, current_cell)
                if current_cell != _cell_to_the_left:
                    ending_cell = cell_to_the_left(crossword, current_cell)

            if ending_cell:
                range_to_the_right = [starting_cell, ending_cell]
                break

            move_cell_to_the_right(current_cell)

    return [r for r in [range_below, range_to_the_right] if r is not None]


def solve(crossword, words):
    pending_words = set(words)
    number_of_rows = len(crossword)
    number_of_columns = len(crossword[0])

    words_by_length = {}
    for word in words:
        word_length = len(word)
        if word_length in words_by_length:
            words_by_length[word_length].append(word)
        else:
            words_by_length[word_length] = [word]

    cells_ranges = make_2d_matrix(number_of_rows, number_of_columns, 0)
    ranges = set()
    for i in range(number_of_rows):
        for j in range(number_of_columns):
            cell = [i, j]
            _cell_to_the_right = cell_to_the_right(cells_ranges, cell)
            _cell_below = cell_below(cells_ranges, cell)

            if is_blank_cell(crossword, cell):
                _ranges = find_ranges_starting_at(crossword, cells_ranges, cell)
                for _range in _ranges:
                    range_key = make_hash_key(_range)
                    ranges.add(range_key)
                    fill_range(cells_ranges, _range, _range)

    range_lengths = {}
    for range_key in ranges:
        _range = parse_hash_key(range_key)
        range_lengths[range_key] = range_length(_range)


    ranges_intersections = {}
    for i in range(number_of_rows):
        for j in range(number_of_columns):
            ranges_in_cell = cells_ranges[i][j]
            if ranges_in_cell and len(ranges_in_cell) > 1:
                ranges_intersections[make_hash_key(ranges_in_cell)] = [i, j]

    possible_range_words = {}
    for range_key, _range_length in range_lengths.items():
        possible_range_words[range_key] = words_by_length[_range_length]

    # 5. for each 'ranges_intersections', check which candidates match the
    #    intersecting character by getting 'range_lenghts' and
    #    'words_by_length', creating 'intersecting_ranges_solutions'
    #
    #    {[[[0 0] [0 3]] [[0 1] [4 1]]] [["BREW" "RANGE"]]}

    # 6. some 'intersecting_ranges_solutions' will only have 1 solution. fill those
    #    and remove them from the set of 'pending_words'

    # 7. for the remaining 'intersecting_ranges_solutions', try all possible
    #    combinations

    return {
        "possible_range_words": possible_range_words,
        "ranges_intersections": ranges_intersections,
        "words_by_length": words_by_length,
        "ranges": ranges,
        "range_lengths": range_lengths,
        "cells_ranges": cells_ranges,
        "crossword": crossword,
    }


pprint(solve(crossword, words))


crossword_input = [
    "+-++++++++",
    "+-++++++++",
    "+-++++++++",
    "+-----++++",
    "+-+++-++++",
    "+-+++-++++",
    "+++++-++++",
    "++------++",
    "+++++-++++",
    "+++++-++++",
    "LONDON;DELHI;ICELAND;ANKARA",
]
crossword = parse_crossword(crossword_input)
words = parse_crossword_words(crossword_input)


def crosswordPuzzle(crossword, words):
    pass


if __name__ == "__main__":
    fptr = open(os.environ["OUTPUT_PATH"], "w")

    crossword = []

    for _ in range(10):
        crossword_item = input()
        crossword.append(crossword_item)

    words = input()

    result = crosswordPuzzle(crossword, words)

    fptr.write("\n".join(result))
    fptr.write("\n")

    fptr.close()
