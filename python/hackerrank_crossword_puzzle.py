#!/bin/python3

from pprint import pprint

from copy import deepcopy
from itertools import permutations
import json
import math
import os
import random
import re
import sys


# helpers.


def hash_object(obj):
    if isinstance(obj, set):
        obj = list(obj)

    return json.dumps(obj)


def unhash_object(key):
    return json.loads(key)


def make_2d_matrix(rows, columns, value):
    return [[value for i in range(rows)] for j in range(columns)]


def parse_crossword_input(crossword_input):
    number_of_rows = len(crossword_input)
    number_of_columns = len(crossword_input[0])
    crossword = make_2d_matrix(number_of_rows, number_of_columns, None)
    for i in range(number_of_rows):
        for j in range(number_of_columns):
            crossword[i][j] = crossword_input[i][j]
    return crossword


def unparse_crossword_input(crossword):
    number_of_rows = len(crossword)
    number_of_columns = len(crossword[0])
    crossword_input = []
    for i in range(number_of_rows):
        crossword_input.append("")
        for j in range(number_of_columns):
            crossword_input[i] += crossword[i][j]
    return crossword_input


def parse_crossword_words_input(words_input):
    return words_input.split(";")


# concepts:
#
#   1. cell
#      a two-element array in the form of '[x, y]'.
#   2. blank cell
#      a crossword cell that needs to be filled with a character.
#   3. range
#      a two-element array in the form of '[start_cell, end_cell]'.
#   4. intersection
#      a cell where two or more ranges intersect.
#
# algorithm:
#
#   1. get a mapping of length to words into 'words_by_length'.
#
#      {4 ["ABBA" "BREW"]
#       5 ["COLIN" "RANGE"]}
#
#   2. get all ranges to be filled in the crossword into 'ranges'.
#
#      [[[0 0] [0 3]]
#       [[0 1] [4 1]]]
#
#   3. get a mapping of ranges to their lengths into 'range_lengths'.
#
#      {[[0 0] [0 3]] 4
#       [[0 1] [4 1]] 5}
#
#   4. get a mapping of intersecting ranges to the cells where they intersect
#      into 'ranges_intersections'.
#
#      {[[[0 0] [0 3]]
#        [[0 1] [4 1]]] [0 1]}
#
#   5. get a mapping of ranges to words which fit them based solely on both
#      the range lengths (via 'range_lengths') and word lengths (via
#      'words_by_length') into 'possible_range_words'.
#
#      {[[0 0] [0 3]] ["ABBA" "BREW"]
#       [[0 1] [4 1]] ["COLIN" "RANGE"]}
#
#   6. some 'possible_range_words' will only have 1 candidate word. fill those
#      and remove them from the set of 'pending_possible_range_words'


BLANK_CELL = "-"


def is_blank_cell(crossword, cell):
    return crossword[cell[0]][cell[1]] == BLANK_CELL


def is_word_cell(crossword, cell):
    char = crossword[cell[0]][cell[1]]
    return char.isalpha() and char.isupper()


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


def fill_matrix_range_with_value(matrix, _range, value):
    start = _range[0]
    end = _range[1]
    for i in range(start[0], end[0] + 1):
        for j in range(start[1], end[1] + 1):
            if matrix[i][j]:
                matrix[i][j].append(value)
            else:
                matrix[i][j] = [value]
    return matrix


def fill_matrix_range_with_string(matrix, _range, string):
    start = _range[0]
    end = _range[1]
    k = 0
    for i in range(start[0], end[0] + 1):
        for j in range(start[1], end[1] + 1):
            matrix[i][j] = string[k]
            k += 1
    return matrix


def string_conflicts_with_range(crossword, _range, string):
    start = _range[0]
    end = _range[1]
    k = 0
    for i in range(start[0], end[0] + 1):
        for j in range(start[1], end[1] + 1):
            if is_word_cell(crossword, [i, j]) and crossword[i][j] != string[k]:
                return True
            k += 1
    return False


def find_crossword_ranges_starting_at(crossword, cells_ranges, starting_cell):
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

            if not is_blank_cell(crossword, current_cell):
                _cell_above = cell_above(crossword, current_cell)
                if current_cell != _cell_above:
                    ending_cell = cell_above(crossword, current_cell)
            elif current_cell[0] == number_of_rows - 1:
                if is_blank_cell(crossword, current_cell):
                    ending_cell = current_cell

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

            if not is_blank_cell(crossword, current_cell):
                _cell_to_the_left = cell_to_the_left(crossword, current_cell)
                if current_cell != _cell_to_the_left:
                    ending_cell = cell_to_the_left(crossword, current_cell)
            elif current_cell[1] == number_of_columns - 1:
                if is_blank_cell(crossword, current_cell):
                    ending_cell = current_cell

            if ending_cell:
                range_to_the_right = [starting_cell, ending_cell]
                break

            move_cell_to_the_right(current_cell)

    return [r for r in [range_below, range_to_the_right] if r is not None]


def solve(crossword, words):
    number_of_rows = len(crossword)
    number_of_columns = len(crossword[0])

    # 1. get a mapping of length to words into 'words_by_length'.
    words_by_length = {}
    for word in words:
        word_length = len(word)
        if word_length in words_by_length:
            words_by_length[word_length].add(word)
        else:
            words_by_length[word_length] = set([word])

    # 2. get all ranges to be filled in the crossword into 'ranges'.
    cells_ranges = make_2d_matrix(number_of_rows, number_of_columns, 0)
    ranges = set()
    for i in range(number_of_rows):
        for j in range(number_of_columns):
            cell = [i, j]
            _cell_to_the_right = cell_to_the_right(cells_ranges, cell)
            _cell_below = cell_below(cells_ranges, cell)

            if is_blank_cell(crossword, cell):
                _ranges = find_crossword_ranges_starting_at(
                    crossword, cells_ranges, cell
                )
                for _range in _ranges:
                    range_key = hash_object(_range)
                    ranges.add(range_key)
                    fill_matrix_range_with_value(cells_ranges, _range, _range)

    # 3. get a mapping of ranges to their lengths into 'range_lengths'.
    range_lengths = {}
    for range_key in ranges:
        _range = unhash_object(range_key)
        range_lengths[range_key] = range_length(_range)

    # 4. get a mapping of intersecting ranges to the cells where they intersect
    #    into 'ranges_intersections'.
    ranges_intersections = {}
    for i in range(number_of_rows):
        for j in range(number_of_columns):
            ranges_in_cell = cells_ranges[i][j]
            if ranges_in_cell and len(ranges_in_cell) > 1:
                ranges_intersections[hash_object(ranges_in_cell)] = [i, j]

    # 5. get a mapping of ranges to words which fit them based solely on both
    #    the range lengths (via 'range_lengths') and word lengths (via
    #    'words_by_length') into 'possible_range_words'.
    possible_range_words = {}
    for range_key, _range_length in range_lengths.items():
        possible_range_words[range_key] = words_by_length[_range_length]

    pending_possible_range_words = deepcopy(possible_range_words)
    solved_crossword = deepcopy(crossword)

    # 6. some 'possible_range_words' will only have 1 candidate word. fill those
    #    and remove them from the set of 'pending_possible_range_words'
    for range_key in list(pending_possible_range_words.keys()):
        possible_words = pending_possible_range_words[range_key]
        if len(possible_words) == 1:
            possible_word = possible_words.pop()
            fill_matrix_range_with_string(
                solved_crossword, unhash_object(range_key), possible_word
            )
            del pending_possible_range_words[range_key]

    generate_attempt(possible_range_words)
    print("starting")
    pprint(solved_crossword)
    pprint(pending_possible_range_words)
    pprint(range_lengths)
    pprint(words_by_length)
    # 7. for the 'pending_possible_range_words', try all combinations
    while len(pending_possible_range_words) > 0:
        for range_key in list(pending_possible_range_words.keys()):
            possible_words = pending_possible_range_words[range_key]
            for word in list(possible_words):
                print("trying word in range", word, range_key)
                _range = unhash_object(range_key)
                if not string_conflicts_with_range(solved_crossword, _range, word):
                    print("filling word", word)
                    fill_matrix_range_with_string(solved_crossword, _range, word)
                    possible_words.remove(word)
                    print("deleting range", range_key)
                    del pending_possible_range_words[range_key]
        pprint(pending_possible_range_words)
        pprint(solved_crossword)

    # {6: {'SYDNEY', 'TURKEY'},
    #  5: {'EGYPT', 'PARIS'}}

    # {'[[0, 1], [5, 1]]': {'SYDNEY', 'TURKEY'},
    #  '[[4, 1], [4, 5]]': {'EGYPT', 'PARIS'},
    #  '[[4, 5], [9, 5]]': {'SYDNEY', 'TURKEY'},
    #  '[[6, 3], [6, 7]]': {'EGYPT', 'PARIS'}}

    # {['SYDNEY', 'TURKEY']: [[[0, 1], [5, 1]], [[4, 5], [9, 5]]]
    #  ['EGYPT', 'PARIS']:   [[[4, 1], [4, 5]], [[6, 3], [6, 7]]]}

    # {[[0, 1], [5, 1]] 'SYDNEY'
    #  [[4, 5], [9, 5]] 'TURKEY'
    #  [[4, 1], [4, 5]] 'EGYPT'
    #  [[6, 3], [6, 7]] 'PARIS'}

    # {[[0, 1], [5, 1]] 'SYDNEY'
    #  [[4, 5], [9, 5]] 'TURKEY'
    #  [[4, 1], [4, 5]] 'PARIS'
    #  [[6, 3], [6, 7]] 'EGYPT'}

    # {[[0, 1], [5, 1]] 'TURKEY'
    #  [[4, 5], [9, 5]] 'SYDNEY'
    #  [[4, 1], [4, 5]] 'EGYPT'
    #  [[6, 3], [6, 7]] 'PARIS'}

    # {[[0, 1], [5, 1]] 'TURKEY'
    #  [[4, 5], [9, 5]] 'SYDNEY'
    #  [[4, 1], [4, 5]] 'PARIS'
    #  [[6, 3], [6, 7]] 'EGYPT'}

    # {'[[0, 1], [5, 1]]': 'TURKEY',
    #  '[[4, 5], [9, 5]]': 'SYDNEY'}

    return [
        "0 - crossword",
        crossword,
        "1 - words_by_length",
        words_by_length,
        "2 - ranges",
        ranges,
        "3 - range_lengths",
        range_lengths,
        "4 - cells_ranges",
        cells_ranges,
        "5 - ranges_intersections",
        ranges_intersections,
        "5 - possible_range_words",
        possible_range_words,
        "6 - pending_possible_range_words",
        pending_possible_range_words,
        "7 - solved_crossword",
        unparse_crossword_input(solved_crossword),
    ]

# 1. for each length, generate its permutations
print(list(permutations([['SYDNEY', 'TURKEY', 'EGYPT', 'PARIS'], ['A']])))

crossword_input_1 = [
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
]
words_input_1 = "LONDON;DELHI;ICELAND;ANKARA"
crossword_input_2 = [
    "+-++++++++",
    "+-++++++++",
    "+-------++",
    "+-++++++++",
    "+-++++++++",
    "+------+++",
    "+-+++-++++",
    "+++++-++++",
    "+++++-++++",
    "++++++++++",
]
words_input_2 = "AGRA;NORWAY;ENGLAND;GWALIOR"
crossword_input_3 = [
    "XXXXXX-XXX",
    "XX------XX",
    "XXXXXX-XXX",
    "XXXXXX-XXX",
    "XXX------X",
    "XXXXXX-X-X",
    "XXXXXX-X-X",
    "XXXXXXXX-X",
    "XXXXXXXX-X",
    "XXXXXXXX-X",
]
words_input_3 = "ICELAND;MEXICO;PANAMA;ALMATY"
crossword_input_4 = [
    "XXXXXX-XXX",
    "XX------XX",
    "XXXXXX-XXX",
    "XXXXXX-XXX",
    "XXX------X",
    "XXXXXX-X-X",
    "XXXXXX-X-X",
    "XXXXXXXX-X",
    "XXXXXXXX-X",
    "XXXXXXXX-X",
]
words_input_4 = "ICELAND;MEXICO;PANAMA;ALMATY"

crossword_input_5 = [
    "+-++++++++",
    "+-++++++++",
    "+-------++",
    "+-++++++++",
    "+-----++++",
    "+-+++-++++",
    "+++-----++",
    "+++++-++++",
    "+++++-++++",
    "+++++-++++",
]
words_input_5 = "SYDNEY;TURKEY;DETROIT;EGYPT;PARIS"
# +S++++++++
# +Y++++++++
# +DETROIT++
# +N++++++++
# +EGYPT++++
# +Y+++U++++
# +++PARIS++
# +++++K++++
# +++++E++++
# +++++Y++++


def crosswordPuzzle(crossword, words):
    # return solve(parse_crossword_input(crossword), parse_crossword_words_input(words))[8][
    #     "7 - solved_crossword"
    # ]
    return solve(parse_crossword_input(crossword), parse_crossword_words_input(words))


# pprint(crosswordPuzzle(crossword_input_1, words_input_1))
# pprint(crosswordPuzzle(crossword_input_2, words_input_2))
# pprint(crosswordPuzzle(crossword_input_3, words_input_3))
# pprint(crosswordPuzzle(crossword_input_4, words_input_4))
pprint(crosswordPuzzle(crossword_input_5, words_input_5))


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
