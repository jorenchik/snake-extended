import numpy.typing as npt
from typing import Any
import math
from snakext.game.state import state_types
import random


def matrix_substring_element_coordinates(
        substring: Any, haystack: npt.NDArray[Any]) -> tuple[int, int]:
    coords = (-1, -1)
    for i, row in enumerate(haystack):
        for k, val in enumerate(row):
            if substring in val:
                coords = i, k
                break
    return coords


def vec_2d_add(vec_1: tuple[float, float],
               vec_2: tuple[float, float]) -> tuple[float, float]:
    return (vec_1[0] + vec_2[0], vec_1[1] + vec_2[1])


def vec_2d_multiply(vec_1: tuple[float, float],
                    vec_2: tuple[float, float]) -> tuple[float, float]:
    return (vec_1[0] * vec_2[0], vec_1[1] * vec_2[1])


def fill_matrix(
    arr: npt.NDArray[Any],
    source_list: list[Any],
    rows: int,
    cols: int,
) -> npt.NDArray[Any]:
    for i in range(0, rows * cols):
        (y_pos, x_pos) = matrix_position_of_index(i, cols)
        arr[y_pos, x_pos] = source_list[i]
    return arr


def matrix_position_of_index(idx: int, cols: int) -> tuple[int, int]:
    x_pos = idx % cols
    y_pos = math.floor(idx / cols)
    return (y_pos, x_pos)


def choose_random_element(
        matrix: state_types.OBJECT_ND_ARRAY) -> tuple[int, int]:
    row_count, col_count = matrix.shape
    random_row = random.randrange(0, row_count - 1, 1)
    random_col = random.randrange(0, col_count - 1, 1)
    return random_row, random_col


def choose_random_match(
        match_: str, matrix: state_types.OBJECT_ND_ARRAY) -> tuple[int, int]:

    available_coords = []
    for i, row in enumerate(matrix):
        for k, place in enumerate(row):
            if place == match_:
                available_coords.append((i, k))
    chosen_coordinates = random.choice(available_coords)
    return chosen_coordinates


def middle_left_element_position(
        matrix: state_types.OBJECT_ND_ARRAY) -> tuple[int, int]:
    row_count, col_count = matrix.shape
    position = (math.floor(row_count / 2), math.floor(col_count / 4))
    return position
