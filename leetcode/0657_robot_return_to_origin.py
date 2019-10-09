#!/usr/bin/env python3

# https://leetcode.com/problems/robot-return-to-origin/

# Runtime: 96 ms, faster than 7.58% of Python3 online submissions for Robot Return to Origin.
# Memory Usage: 14 MB, less than 6.90% of Python3 online submissions for Robot Return to Origin.


def move_up(coordinates):
    coordinates[1] += 1
    return coordinates


def move_down(coordinates):
    coordinates[1] -= 1
    return coordinates


def move_left(coordinates):
    coordinates[0] -= 1
    return coordinates


def move_right(coordinates):
    coordinates[0] += 1
    return coordinates


MOVEMENTS = {"U": move_up, "D": move_down, "L": move_left, "R": move_right}


def follow(starting_coordinates, movements):
    coordinates = [x for x in starting_coordinates]

    for movement in movements:
        coordinates = MOVEMENTS[movement](coordinates)

    return coordinates


class Solution:
    def judgeCircle(self, moves: str) -> bool:
        starting_coordinates = [0, 0]
        return starting_coordinates == follow(starting_coordinates, moves)
