""" Contains all the state of the game. """

import numpy as np
import numpy.typing as npt
from dataclasses import dataclass
from snakext.utils import math_
from snakext import state_types

VOID_PLACE = 'v'
FOOD_PLACE = 'f'
SNAKE_BODY_PLACE = 'b'
SNAKE_TAIL_PLACE = 't'
SNAKE_HEAD_PLACE = 'h'
SNAKE_PLACES: list[str] = [
    SNAKE_TAIL_PLACE, SNAKE_BODY_PLACE, SNAKE_HEAD_PLACE
]

TOP_DIRECTION = 1
BOTTOM_DIRECTION = 2
RIGHT_DIRECTION = 3
LEFT_DIRECTION = 4


@dataclass
class State:
    snake_placement: state_types.OBJECT_ND_ARRAY
    food_placement: state_types.OBJECT_ND_ARRAY
    movement_direction: int
    previous_snake_placement: state_types.OBJECT_ND_ARRAY


state_instance: State


def init_state(grid_rows: int, grid_cols: int) -> State:
    global state_instance
    grid_shape = (grid_rows, grid_cols)
    element_count = grid_shape[0] * grid_shape[1]
    snake_placement = np.empty(grid_shape, dtype=np.object_)
    food_placement = np.empty(grid_shape, dtype=np.object_)
    grid_contents = ['v' for x in range(element_count)]
    math_.fill_arr_2d(snake_placement, grid_contents, *grid_shape)
    math_.fill_arr_2d(food_placement, grid_contents, *grid_shape)
    # Choose some direction for the snake
    state_instance = State(
        snake_placement,
        food_placement,
        RIGHT_DIRECTION,
        snake_placement,
    )
    return state_instance
