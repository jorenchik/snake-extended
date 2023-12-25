""" Contains all the state of the game. """

import numpy as np
from dataclasses import dataclass
from snakext.game.state import state_types

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
class TransmittedState:
    snake_placement: list[tuple[int, int]]


@dataclass
class State:
    local_snake_placement: state_types.OBJECT_ND_ARRAY
    remote_snake_placement: state_types.OBJECT_ND_ARRAY
    food_placement: state_types.OBJECT_ND_ARRAY
    movement_direction: int
    previous_snake_placement: state_types.OBJECT_ND_ARRAY
    add_do_snake: bool
    multiplayer: bool


state_instance: State | None
local_transmitted_state_instance: TransmittedState | None
remote_transmitted_state_instance: TransmittedState | None


def init_state(grid_rows: int,
               grid_cols: int,
               multiplayer: bool = False) -> State:
    global state_instance
    grid_shape = (grid_rows, grid_cols)
    local_snake_placement = np.full(grid_shape, 'v', dtype=np.object_)
    remote_snake_placement = np.full(grid_shape, 'v', dtype=np.object_)
    food_placement = np.full(grid_shape, 'v', dtype=np.object_)
    # Choose some direction for the snake
    state_instance = State(
        local_snake_placement=local_snake_placement,
        remote_snake_placement=remote_snake_placement,
        previous_snake_placement=local_snake_placement,
        add_do_snake=False,
        food_placement=food_placement,
        movement_direction=RIGHT_DIRECTION,
        multiplayer=multiplayer,
    )
    return state_instance


def init_transmitted_state() -> TransmittedState:
    return TransmittedState(snake_placement=[])
