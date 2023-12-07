""" Contains all the state of the game. """

import numpy as np
import numpy.typing as npt
from dataclasses import dataclass
from snakext.views import game_view
from snakext.utils import math_

VOID_PLACE = 'v'
SNAKE_BODY_PLACE = 'b'
SNAKE_TAIL_PLACE = 't'
SNAKE_HEAD_PLACE = 'h'
SNAKE_PLACES: list[str] = [
    SNAKE_TAIL_PLACE, SNAKE_BODY_PLACE, SNAKE_HEAD_PLACE
]


@dataclass
class State:
    snake_placement: npt.NDArray[np.str_]


state_instance: State


def init_state() -> None:
    global state_instance
    grid_shape = (game_view.playground_instance.grid_rows,
                  game_view.playground_instance.grid_cols)
    element_count = grid_shape[0] * grid_shape[1]
    snake_placement = np.empty(grid_shape, dtype=np.str_)
    grid_contents = ['v' for x in range(element_count)]
    math_.fill_arr_2d(snake_placement, grid_contents, *grid_shape)
    state_instance = State(snake_placement)
