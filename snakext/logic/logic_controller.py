""" Calculates the game logic concerns """
import numpy as np
from snakext.state import state
from snakext.utils import math_

TOP_DIRECTION = 1
BOTTOM_DIRECTION = 2
RIGHT_DIRECTION = 3
LEFT_DIRECTION = 4

POSSIBLE_OFFSETS = {
    RIGHT_DIRECTION: (0, -1),
    TOP_DIRECTION: (1, 0),
    LEFT_DIRECTION: (0, 1),
    BOTTOM_DIRECTION: (-1, 0)
}


def move_snake(
    snake_placement: np.ndarray[tuple[int, int], np.dtype[np.object_]],
    key: int,
) -> np.ndarray[tuple[int, int], np.dtype[np.str_]]:
    return snake_placement


def get_direction(
        snake_placement: np.ndarray[tuple[int, int],
                                    np.dtype[np.object_]]) -> int:
    head_position = index_2d_arr_from_val(snake_placement,
                                          f"{state.SNAKE_HEAD_PLACE}1")
    direction = _find_element_with_offset_from_pos(
        snake_placement, POSSIBLE_OFFSETS, head_position,
        f"{state.SNAKE_BODY_PLACE}2")
    return direction if direction else 0


def index_2d_arr_from_val(arr_2d: np.ndarray[tuple[int, int],
                                             np.dtype[np.object_]],
                          value: str) -> tuple[int, int]:
    head_position = None
    for i, row in enumerate(arr_2d):
        for k, place in enumerate(row):
            if place == value:
                head_position = (i, k)
    return head_position if head_position else (-1, -1)


def _find_element_with_offset_from_pos(arr_2d: np.ndarray[tuple[
    int, int], np.dtype[np.object_]], offsets: dict[int, tuple[int, int]],
                                       position: tuple[int, int],
                                       searched_str: str) -> int | None:
    key = None
    for supposed_direction, offset in offsets.items():
        (y, x) = math_.vec_2d_add(position, offset)
        shape = arr_2d.shape
        if y == -1 or x == -1 or y == shape[0] or x == shape[1]:
            continue
        if arr_2d[int(y), int(x)] == searched_str:
            key = supposed_direction
            break
    if not key:
        raise ValueError("Head is not found for a snake")
    return key
