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
COORDINATES_NOT_FOUND = (-1, -1)


def handle_food_collision(
    snake_placement: STRING_2D_ARR_TYPE,
    food_placement: STRING_2D_ARR_TYPE,
) -> tuple[STRING_2D_ARR_TYPE, bool]:
    collision_coordinates = _search_collision(snake_placement,
                                              food_placement,
                                              only_head=True)
    collided = False
    if collision_coordinates != COORDINATES_NOT_FOUND:
        collided = True
        food_placement[collision_coordinates] = state.VOID_PLACE
    return (food_placement, collided)


def _middle_left(matrix: STRING_2D_ARR_TYPE) -> tuple[int, int]:
    row_count, col_count = matrix.shape
    position = (math.floor(row_count / 2), math.floor(col_count / 4))
    return position


def _choose_random(matrix: STRING_2D_ARR_TYPE) -> tuple[int, int]:
    row_count, col_count = matrix.shape
    random_row = random.randrange(0, row_count - 1, 1)
    random_col = random.randrange(0, col_count - 1, 1)
    return random_row, random_col


def _choose_match(match_: str, matrix: STRING_2D_ARR_TYPE) -> tuple[int, int]:

    available_coords = []
    for i, row in enumerate(matrix):
        for k, place in enumerate(row):
            if place == match_:
                available_coords.append((i, k))
    chosen_coordinates = random.choice(available_coords)
    return chosen_coordinates


def place_food(
    food_placement: STRING_2D_ARR_TYPE,
    other_placement: STRING_2D_ARR_TYPE,
    choose_coordinates: typing.Callable[[str, STRING_2D_ARR_TYPE],
                                        tuple[int, int]] = _choose_match,
    where_to_place: str = state.VOID_PLACE,
) -> STRING_2D_ARR_TYPE:
    i, k = choose_coordinates(where_to_place, food_placement)
    food_placement[i, k] = state.FOOD_PLACE
    return food_placement


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
    incremented_number = int(place[1:]) + 1
    place = f"{place[0]}{incremented_number}"
    return place


def move_snake(
    snake_placement: STRING_2D_ARR_TYPE,
    movement_direction: int,
    movement_key: int,
    add_to_snake: bool = False,
) -> tuple[STRING_2D_ARR_TYPE, int, bool]:
    new_snake_placement = np.copy(snake_placement)

    head_coords = math_.coords_strstr(state.SNAKE_HEAD_PLACE,
                                      new_snake_placement)
    tail_coords = math_.coords_strstr(state.SNAKE_TAIL_PLACE,
                                      new_snake_placement)
    tail_place = new_snake_placement[tail_coords]
    tail_number = int(tail_place[1:])
    new_tail_coords = math_.coords_strstr(
        f"{state.SNAKE_BODY_PLACE}{tail_number - 1}", new_snake_placement)
    new_snake_placement[head_coords] = _change_place(
        new_snake_placement[head_coords], state.SNAKE_BODY_PLACE, number=0)
    new_snake_placement = _increment_snake_places(new_snake_placement)
    if movement_key == 0:
        movement_key = movement_direction
    movement_direction_vector = MOVEMENT_DIRECTIONS[movement_direction]
    movement_vector = MOVEMENT_DIRECTIONS[movement_key]
    if not _is_opposite(movement_direction_vector, movement_vector):
        movement_direction = movement_key
    else:
        movement_vector = movement_direction_vector

    new_snake_placement, movement_successful = _move_head(
        new_snake_placement, head_coords, movement_vector)

    if not add_to_snake and movement_successful:
        new_snake_placement[tail_coords] = state.VOID_PLACE
        new_snake_placement[new_tail_coords] = _change_place(
            new_snake_placement[new_tail_coords], state.SNAKE_TAIL_PLACE,
            tail_number)

    if not movement_successful:
        new_snake_placement = snake_placement

    return new_snake_placement, movement_direction, movement_successful


def check_for_headless(snake_placement: STRING_2D_ARR_TYPE) -> bool:
    return math_.coords_strstr(state.SNAKE_HEAD_PLACE,
                               snake_placement) != COORDINATES_NOT_FOUND


def headless_placement(snake_placement: STRING_2D_ARR_TYPE):
    head_coords = math_.coords_strstr(state.SNAKE_HEAD_PLACE, snake_placement)
    headless_placement = snake_placement
    if head_coords != COORDINATES_NOT_FOUND:
        headless_placement = np.copy(snake_placement)
        headless_placement[head_coords] = state.VOID_PLACE
    return headless_placement


def check_collision(placement1: STRING_2D_ARR_TYPE,
                    placement2: STRING_2D_ARR_TYPE,
                    only_head: bool = True) -> bool:
    collision_found = _search_collision(
        placement1, placement2, only_head=only_head) != COORDINATES_NOT_FOUND
    return collision_found


def _search_collision(placement1: STRING_2D_ARR_TYPE,
                      placement2: STRING_2D_ARR_TYPE,
                      only_head: bool = False) -> tuple[int, int]:
    coordinates = COORDINATES_NOT_FOUND
    for i, row in enumerate(placement1):
        for k, place in enumerate(row):
            if (not only_head or placement1[i, k][0] == state.SNAKE_HEAD_PLACE
                ) and placement1[i, k] != state.VOID_PLACE and placement2[
                    i, k] != state.VOID_PLACE:
                coordinates = (i, k)
                break
    return coordinates


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


def _move_head(
        snake_placement: STRING_2D_ARR_TYPE, snake_head_coords: tuple[int,
                                                                      int],
        movement_vector: tuple[int, int]) -> tuple[STRING_2D_ARR_TYPE, bool]:
    new_snake_head_coords = (snake_head_coords[0] + movement_vector[0],
                             snake_head_coords[1] + movement_vector[1])
    dim_y, dim_x = snake_placement.shape
    new_snake_head_coords = (new_snake_head_coords[0] % dim_y,
                             new_snake_head_coords[1] % dim_x)
    is_occupied = snake_placement[new_snake_head_coords] != state.VOID_PLACE
    if not is_occupied:
        snake_placement[new_snake_head_coords] = HEAD_PLACE
    return snake_placement, not is_occupied


def _change_place(place: str,
                  letter: str | None = None,
                  number: int = -1) -> str:
    letter = letter if letter else place[0]
    number = number if number != -1 else int(place[1])
    new_place = f"{letter}{number}"
    return new_place
