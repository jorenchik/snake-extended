""" Calculates the game logic concerns """
import numpy as np
from snakext.state import state
from snakext.facades import pygame_facade
import typing
import random
from snakext.utils import math_
import math

MOVEMENT_DIRECTIONS = {
    state.RIGHT_DIRECTION: (0, 1),
    state.TOP_DIRECTION: (-1, 0),
    state.LEFT_DIRECTION: (0, -1),
    state.BOTTOM_DIRECTION: (1, 0)
}

STRING_2D_ARR_TYPE = np.ndarray[tuple[int, int], np.dtype[np.object_]]
HEAD_PLACE = f"{state.SNAKE_HEAD_PLACE}0"
INITIAL_BODY_PLACE = f"{state.SNAKE_BODY_PLACE}1"
INITIAL_TAIL_PLACE = f"{state.SNAKE_TAIL_PLACE}2"


def _middle_left(matrix: STRING_2D_ARR_TYPE) -> tuple[int, int]:
    row_count, col_count = matrix.shape
    position = (math.floor(row_count / 2), math.floor(col_count / 4))
    return position


def _choose_random(matrix: STRING_2D_ARR_TYPE) -> tuple[int, int]:
    row_count, col_count = matrix.shape
    random_row = random.randrange(0, row_count - 1, 1)
    random_col = random.randrange(0, col_count - 1, 1)
    return random_row, random_col


def place_initial_snake(
    snake_placement: STRING_2D_ARR_TYPE,
    choose_coordinates: typing.Callable[[STRING_2D_ARR_TYPE],
                                        tuple[int, int]] = _middle_left
) -> STRING_2D_ARR_TYPE:
    initial_places = [
        el for row in snake_placement for el in row if el == HEAD_PLACE
    ]
    if len(initial_places) > 0:
        raise ValueError("Snake is already initialized.")
    i, k = choose_coordinates(snake_placement)

    snake_placement[i, k + 1] = HEAD_PLACE
    snake_placement[i, k] = INITIAL_BODY_PLACE
    snake_placement[i, k - 1] = INITIAL_TAIL_PLACE
    return snake_placement


def _increment_place(place: str) -> str:
    incremented_number = int(place[1]) + 1
    place = f"{place[0]}{incremented_number}"
    return place


def move_snake(
    snake_placement: STRING_2D_ARR_TYPE,
    movement_direction: int,
    movement_key: int,
) -> tuple[STRING_2D_ARR_TYPE, int]:
    head_coords = math_.coords_strstr(state.SNAKE_HEAD_PLACE, snake_placement)
    tail_coords = math_.coords_strstr(state.SNAKE_TAIL_PLACE, snake_placement)
    tail_place = snake_placement[tail_coords]
    tail_number = int(tail_place[1])
    new_tail_coords = math_.coords_strstr(
        f"{state.SNAKE_BODY_PLACE}{tail_number - 1}", snake_placement)
    snake_placement[head_coords] = _change_place(snake_placement[head_coords],
                                                 state.SNAKE_BODY_PLACE,
                                                 number=0)
    snake_placement = _increment_snake_places(snake_placement)
    if movement_key == 0:
        movement_key = movement_direction
    movement_direction_vector = MOVEMENT_DIRECTIONS[movement_direction]
    movement_vector = MOVEMENT_DIRECTIONS[movement_key]
    if not _is_opposite(movement_direction_vector, movement_vector):
        movement_direction = movement_key
    else:
        movement_vector = movement_direction_vector
    snake_placement = _move_head(snake_placement, head_coords, movement_vector)
    snake_placement[tail_coords] = state.VOID_PLACE
    snake_placement[new_tail_coords] = _change_place(
        snake_placement[new_tail_coords], state.SNAKE_TAIL_PLACE, tail_number)
    return snake_placement, movement_direction


def _is_opposite(vec1: tuple[int, int], vec2: tuple[int, int]) -> bool:
    opposite: bool = (vec1[0] == -vec2[0]) and (vec1[1] == -vec2[1])
    return opposite


def _increment_snake_places(
        snake_placement: STRING_2D_ARR_TYPE) -> STRING_2D_ARR_TYPE:
    initial_shape = snake_placement.shape
    snake_placement = np.array([
        _increment_place(place) if place != state.VOID_PLACE else place
        for row in snake_placement for place in row
    ]).reshape(initial_shape)
    return snake_placement


def _move_head(snake_placement: STRING_2D_ARR_TYPE,
               snake_head_coords: tuple[int, int],
               movement_vector: tuple[int, int]) -> STRING_2D_ARR_TYPE:
    new_snake_head_coords = (snake_head_coords[0] + movement_vector[0],
                             snake_head_coords[1] + movement_vector[1])
    dim_y, dim_x = snake_placement.shape
    new_snake_head_coords = (new_snake_head_coords[0] % dim_y,
                             new_snake_head_coords[1] % dim_x)
    snake_placement[new_snake_head_coords] = HEAD_PLACE
    return snake_placement


def _change_place(place: str,
                  letter: str | None = None,
                  number: int = -1) -> str:
    letter = letter if letter else place[0]
    number = number if number != -1 else int(place[1])
    new_place = f"{letter}{number}"
    return new_place
