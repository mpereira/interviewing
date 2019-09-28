#!/usr/bin/env python3

from pprint import pprint
from typing import List


def rectangle_exists(
    coordinates: List[List[int]],
    number_of_rows: int,
    number_of_columns: int,
    starting_coordinates: List[int],
    ending_coordinates: List[int],
) -> List[List[int]]:
    starting_row = starting_coordinates[0]
    starting_column = starting_coordinates[1]
    ending_row = ending_coordinates[0]
    ending_column = ending_coordinates[1]
    if (
        coordinates[starting_row][starting_column] == 1
        and coordinates[ending_row][starting_column] == 1
        and coordinates[starting_row][ending_column] == 1
        and coordinates[ending_row][ending_column] == 1
    ):
        return True

    return False


def rectangles_starting_at(
    coordinates: List[List[int]],
    number_of_rows: int,
    number_of_columns: int,
    starting_coordinates: List[int],
) -> List[List[int]]:
    starting_row = starting_coordinates[0]
    starting_column = starting_coordinates[1]
    rectangles = []
    for row in range(starting_row + 1, number_of_rows):
        for column in range(starting_column + 1, number_of_columns):
            current_coordinates = [row, column]
            if rectangle_exists(
                coordinates,
                number_of_rows,
                number_of_columns,
                starting_coordinates,
                current_coordinates,
            ):
                rectangles.append([starting_coordinates, current_coordinates])
    return rectangles


def rectangles(coordinates: List[List[int]]) -> List[List[int]]:
    number_of_rows = len(coordinates)
    number_of_columns = len(coordinates[0])
    rectangles = []

    for row in range(number_of_rows):
        for column in range(number_of_columns):
            current_rectangles = rectangles_starting_at(
                coordinates, number_of_rows, number_of_columns, [row, column]
            )
            rectangles.extend(current_rectangles)
    return rectangles


coordinates = [
    [1, 1, 0, 1],
    [1, 1, 0, 1],
    [1, 0, 0, 0],
    [0, 1, 0, 1],
    [0, 0, 0, 0],
]


pprint(rectangles(coordinates))
