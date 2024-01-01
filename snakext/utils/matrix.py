"""
This module provides utility functions for matrix operations used in a game
environment. It includes functions for finding specific elements, filling 
matrices, and selecting positions based on various criteria. These utilities 
are designed to manipulate and interact with game state arrays, facilitating 
key game mechanics such as random element placement and coordinate calculations.
"""
import numpy.typing as npt
from typing import Any
import math
from snakext.game.state import state_types
import random


def matrix_substring_element_coordinates(
        substring: Any, haystack: npt.NDArray[Any]) -> tuple[int, int]:
    """
    Finds the coordinates of the first occurrence of a substring in a matrix.

    Args:
        substring (Any): The substring to find in the matrix.
        haystack (npt.NDArray[Any]): The matrix to search within.

    Returns:
        tuple[int, int]: The coordinates of the substring, or (-1, -1) if not found.
    """
    coords = (-1, -1)
    for i, row in enumerate(haystack):
        for k, val in enumerate(row):
            if substring in val:
                coords = i, k
                break
    return coords


def fill_matrix(
    arr: npt.NDArray[Any],
    source_list: list[Any],
    rows: int,
    cols: int,
) -> npt.NDArray[Any]:
    """
    Fills a matrix with elements from a source list.

    Args:
        arr (npt.NDArray[Any]): The matrix to be filled.
        source_list (list[Any]): The list of elements used to fill the matrix.
        rows (int): The number of rows in the matrix.
        cols (int): The number of columns in the matrix.

    Returns:
        npt.NDArray[Any]: The filled matrix.
    """
    for i in range(0, rows * cols):
        (y_pos, x_pos) = matrix_position_of_index(i, cols)
        arr[y_pos, x_pos] = source_list[i]
    return arr


def matrix_position_of_index(idx: int, cols: int) -> tuple[int, int]:
    """
    Calculates the matrix coordinates corresponding to a linear index.

    Args:
        idx (int): The linear index.
        cols (int): The number of columns in the matrix.

    Returns:
        tuple[int, int]: The (row, column) coordinates in the matrix.
    """
    x_pos = idx % cols
    y_pos = math.floor(idx / cols)
    return (y_pos, x_pos)


def choose_random_element(
        matrix: state_types.OBJECT_ND_ARRAY) -> tuple[int, int]:
    """
    Selects a random element's position from a matrix.

    Args:
        matrix (state_types.OBJECT_ND_ARRAY): The matrix to choose from.

    Returns:
        tuple[int, int]: The coordinates of the randomly selected element.
    """
    row_count, col_count = matrix.shape
    random_row = random.randrange(0, row_count - 1, 1)
    random_col = random.randrange(0, col_count - 1, 1)
    return random_row, random_col


def choose_random_match(
        match_: str, matrix: state_types.OBJECT_ND_ARRAY) -> tuple[int, int]:
    """
    Chooses a random position in the matrix where the element matches the specified value.

    Args:
        match_ (str): The value to match in the matrix.
        matrix (state_types.OBJECT_ND_ARRAY): The matrix to search.

    Returns:
        tuple[int, int]: The coordinates of a randomly chosen element matching the specified value.
    """
    available_coords = []
    for i, row in enumerate(matrix):
        for k, place in enumerate(row):
            if place == match_:
                available_coords.append((i, k))
    chosen_coordinates = random.choice(available_coords)
    return chosen_coordinates


def middle_left_element_position(
        matrix: state_types.OBJECT_ND_ARRAY) -> tuple[int, int]:
    """
    Calculates the position in the middle-left part of the matrix.

    Args:
        matrix (state_types.OBJECT_ND_ARRAY): The matrix to calculate the position for.

    Returns:
        tuple[int, int]: The middle-left position in the matrix.
    """
    row_count, col_count = matrix.shape
    position = (math.floor(row_count / 2), math.floor(col_count / 4))
    return position


def middle_right_element_position(
        matrix: state_types.OBJECT_ND_ARRAY) -> tuple[int, int]:
    """
    Calculates the position in the middle-right part of the matrix.

    Args:
        matrix (state_types.OBJECT_ND_ARRAY): The matrix to calculate the position for.

    Returns:
        tuple[int, int]: The middle-right position in the matrix.
    """
    row_count, col_count = matrix.shape
    position = (math.floor(row_count / 2), math.floor(col_count / 4) * 3)
    return position
