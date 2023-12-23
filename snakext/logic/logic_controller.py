""" Calculates the game logic concerns """
import numpy as np
from snakext.state import state
from snakext.facades import pygame_facade

POSSIBLE_OFFSETS = {
    state.RIGHT_DIRECTION: (0, -1),
    state.TOP_DIRECTION: (1, 0),
    state.LEFT_DIRECTION: (0, 1),
    state.BOTTOM_DIRECTION: (-1, 0)
}


def move_snake(
    snake_placement: np.ndarray[tuple[int, int], np.dtype[np.str_]],
    key: int,
) -> np.ndarray[tuple[int, int], np.dtype[np.str_]]:
    return snake_placement


def movement_direction() -> int:
    return 1
