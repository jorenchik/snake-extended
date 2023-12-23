""" Calculates the game logic concerns """
import numpy as np
from snakext.state import state
from snakext.facades import pygame_facade
import typing
import random

POSSIBLE_OFFSETS = {
    state.RIGHT_DIRECTION: (0, -1),
    state.TOP_DIRECTION: (1, 0),
    state.LEFT_DIRECTION: (0, 1),
    state.BOTTOM_DIRECTION: (-1, 0)
}

STRING_2D_ARR_TYPE = np.ndarray[tuple[int, int], np.dtype[np.object_]]
INITIAL_SNAKE_STRING = 'h0'


def _choose_random(matrix: STRING_2D_ARR_TYPE) -> tuple[int, int]:
    row_count, col_count = matrix.shape
    random_row = random.randrange(0, row_count - 1, 1)
    random_col = random.randrange(0, col_count - 1, 1)
    return random_row, random_col


def place_initial_snake(
    snake_placement: STRING_2D_ARR_TYPE,
    choose_coordinates: typing.Callable[[STRING_2D_ARR_TYPE],
                                        tuple[int, int]] = _choose_random
) -> STRING_2D_ARR_TYPE:
    initial_places = [
        el for row in snake_placement for el in row
        if el == INITIAL_SNAKE_STRING
    ]
    if len(initial_places) > 0:
        raise ValueError("Snake is already initialized.")
    i, k = choose_coordinates(snake_placement)
    snake_placement[i, k] = INITIAL_SNAKE_STRING
    return snake_placement


def move_snake(
    snake_placement: STRING_2D_ARR_TYPE,
    key: int,
) -> STRING_2D_ARR_TYPE:
    return snake_placement


def movement_direction() -> int:
    return 1
