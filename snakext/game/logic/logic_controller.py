"""
This module calculates the game logic for a snake game. It includes functions 
for handling food and snake collisions, placing the snake and food on the game
grid, and updating the snake's movement and position. The module uses numpy for
array manipulations and state management to track the game state.
"""
import numpy as np
import typing
from snakext.game.state import state_types
from snakext.utils import game_clock
from snakext.game.state import state
from snakext.utils import matrix

MOVEMENT_DIRECTIONS = {
    state.RIGHT_DIRECTION: (0, 1),
    state.TOP_DIRECTION: (-1, 0),
    state.LEFT_DIRECTION: (0, -1),
    state.BOTTOM_DIRECTION: (1, 0)
}

HEAD_PLACE = f"{state.SNAKE_HEAD_PLACE}0"
INITIAL_BODY_PLACE = f"{state.SNAKE_BODY_PLACE}1"
INITIAL_TAIL_PLACE = f"{state.SNAKE_TAIL_PLACE}2"
COORDINATES_NOT_FOUND = (-1, -1)


def handle_food_collision(
    snake_placement: state_types.OBJECT_ND_ARRAY,
    food_placement: state_types.OBJECT_ND_ARRAY,
) -> tuple[state_types.OBJECT_ND_ARRAY, bool]:
    """
    Checks and handles collisions between the snake and food.

    Args:
        snake_placement (state_types.OBJECT_ND_ARRAY): The current placement of the snake.
        food_placement (state_types.OBJECT_ND_ARRAY): The current placement of the food.

    Returns:
        tuple[state_types.OBJECT_ND_ARRAY, bool]: Updated food placement and a flag indicating collision.
    """
    collision_coordinates = _search_collision(snake_placement,
                                              food_placement,
                                              only_head=False)
    collided = False
    if collision_coordinates != COORDINATES_NOT_FOUND:
        collided = True
        food_placement[collision_coordinates] = state.VOID_PLACE
    return (food_placement, collided)


def check_remote_snake_collision(
    local_snake_placement: state_types.OBJECT_ND_ARRAY,
    remote_snake_placement: state_types.OBJECT_ND_ARRAY,
) -> bool:
    """
    Checks for collisions between the local snake and a remote snake.

    Args:
        local_snake_placement (state_types.OBJECT_ND_ARRAY): The placement of the local snake.
        remote_snake_placement (state_types.OBJECT_ND_ARRAY): The placement of the remote snake.

    Returns:
        bool: True if there is a collision, False otherwise.
    """
    collision_coordinates = _search_collision(local_snake_placement,
                                              remote_snake_placement,
                                              only_head=False)
    return collision_coordinates != COORDINATES_NOT_FOUND


def place_food(
    food_placement: state_types.OBJECT_ND_ARRAY,
    other_placement: state_types.OBJECT_ND_ARRAY,
    choose_coordinates: typing.Callable[
        [str, state_types.OBJECT_ND_ARRAY],
        tuple[int, int]] = matrix.choose_random_match,
    where_to_place: str = state.VOID_PLACE,
) -> bool:
    """
    Places food on the grid in a location not occupied by the snake.

    Args:
        food_placement (state_types.OBJECT_ND_ARRAY): The current placement of the food.
        other_placement (state_types.OBJECT_ND_ARRAY): The placement of the snake or other objects.
        choose_coordinates (Callable): Function to choose coordinates for placing food.
        where_to_place (str): The type of place to search for placement.

    Returns:
        bool: whether the food was placed successfully
    """
    i, k = choose_coordinates(where_to_place, food_placement)
    place_found = (i, k) != COORDINATES_NOT_FOUND
    if place_found:
        food_placement[i, k] = state.FOOD_PLACE
    return place_found


def placement_array(
        placement: state_types.OBJECT_ND_ARRAY) -> list[tuple[int, int]]:
    placement_arr: list[tuple[int, int]] = []
    """
    Converts a placement grid into a list of coordinates.

    Args:
        placement (state_types.OBJECT_ND_ARRAY): The placement grid to convert.

    Returns:
        list[tuple[int, int]]: A list of coordinates where objects are placed.
    """
    for i, row in enumerate(placement):
        for k, place in enumerate(row):
            if place != state.VOID_PLACE:
                placement_arr.append((i, k))
    return placement_arr


def placement_from_array(
    placement_arr: list[tuple[int, int]],
    shape: tuple[int, int],
    place_str: str,
) -> state_types.OBJECT_ND_ARRAY:
    """
    Converts a list of coordinates back into a placement grid.

    Args:
        placement_arr (list[tuple[int, int]]): List of coordinates.
        shape (tuple[int, int]): Shape of the grid.
        place_str (str): String identifier for the placement.

    Returns:
        state_types.OBJECT_ND_ARRAY: The reconstructed placement grid.
    """
    placement = np.full(shape, state.VOID_PLACE, dtype=np.object_)
    for i, row in enumerate(placement):
        for k, place in enumerate(row):
            if [i, k] in placement_arr:
                placement[i, k] = place_str
    return placement


def place_initial_snake(
    snake_placement: state_types.OBJECT_ND_ARRAY,
    choose_coordinates: typing.Callable[[state_types.OBJECT_ND_ARRAY], tuple[
        int, int]] = matrix.middle_left_element_position
) -> state_types.OBJECT_ND_ARRAY:
    """
    Places the initial snake on the grid.

    Args:
        snake_placement (state_types.OBJECT_ND_ARRAY): The grid to place the snake on.
        choose_coordinates (Callable): Function to choose the initial coordinates for the snake.

    Returns:
        state_types.OBJECT_ND_ARRAY: Updated grid with the initial snake placement.

    Raises:
        ValueError: If the snake is already initialized.
    """
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
    snake_placement: state_types.OBJECT_ND_ARRAY,
    movement_direction: int,
    movement_key: int,
    add_to_snake: bool = False,
) -> tuple[state_types.OBJECT_ND_ARRAY, int, bool]:
    """
    Moves the snake in the given direction.

    Args:
        snake_placement (state_types.OBJECT_ND_ARRAY): Current snake placement.
        movement_direction (int): The current direction of movement.
        movement_key (int): The new direction of movement.
        add_to_snake (bool): Flag to indicate whether to grow the snake.

    Returns:
        tuple[state_types.OBJECT_ND_ARRAY, int, bool]: New snake placement, new movement direction, and success flag.
    """
    new_snake_placement = np.copy(snake_placement)

    tail_coords = matrix.matrix_substring_element_coordinates(
        state.SNAKE_TAIL_PLACE, new_snake_placement)
    tail_place = new_snake_placement[tail_coords]
    tail_number = int(tail_place[1:])
    new_tail_coords = matrix.matrix_substring_element_coordinates(
        f"{state.SNAKE_BODY_PLACE}{tail_number - 1}", new_snake_placement)

    head_coords = matrix.matrix_substring_element_coordinates(
        state.SNAKE_HEAD_PLACE, new_snake_placement)
    new_snake_placement[head_coords] = _change_place(
        new_snake_placement[head_coords], state.SNAKE_BODY_PLACE, number=0)
    movement_key, movement_direction, movement_vector = _movement_attributes(
        movement_direction,
        movement_key,
    )

    new_snake_placement = _increment_snake_places(new_snake_placement)
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


def _movement_attributes(
    movement_direction: int,
    movement_key: int,
) -> tuple[int, int, tuple[int, int]]:
    if movement_key == 0:
        movement_key = movement_direction
    movement_direction_vector = MOVEMENT_DIRECTIONS[movement_direction]
    movement_vector = MOVEMENT_DIRECTIONS[movement_key]
    if not _is_opposite(movement_direction_vector, movement_vector):
        movement_direction = movement_key
    else:
        movement_vector = movement_direction_vector
    return movement_key, movement_direction, movement_vector


def check_for_headless(snake_placement: state_types.OBJECT_ND_ARRAY) -> bool:
    """
    Checks if the snake is headless in the current placement.

    Args:
        snake_placement (state_types.OBJECT_ND_ARRAY): The current snake placement.

    Returns:
        bool: True if the snake is headless, False otherwise.
    """
    return matrix.matrix_substring_element_coordinates(
        state.SNAKE_HEAD_PLACE, snake_placement) != COORDINATES_NOT_FOUND


def headless_placement(
    snake_placement: state_types.OBJECT_ND_ARRAY
) -> state_types.OBJECT_ND_ARRAY:
    """
    Generates a placement grid for the snake without its head.

    Args:
        snake_placement (state_types.OBJECT_ND_ARRAY): The current snake placement.

    Returns:
        state_types.OBJECT_ND_ARRAY: The snake placement without the head.
    """
    head_coords = matrix.matrix_substring_element_coordinates(
        state.SNAKE_HEAD_PLACE, snake_placement)
    headless_placement = snake_placement
    if head_coords != COORDINATES_NOT_FOUND:
        headless_placement = np.copy(snake_placement)
        headless_placement[head_coords] = state.VOID_PLACE
    return headless_placement


def check_collision(placement1: state_types.OBJECT_ND_ARRAY,
                    placement2: state_types.OBJECT_ND_ARRAY,
                    only_head: bool = True) -> bool:
    """
    Checks for a collision between two placements.

    Args:
        placement1 (state_types.OBJECT_ND_ARRAY): First placement grid.
        placement2 (state_types.OBJECT_ND_ARRAY): Second placement grid.
        only_head (bool): Flag to consider only the head for collision.

    Returns:
        bool: True if there is a collision, False otherwise.
    """
    collision_found = _search_collision(
        placement1, placement2, only_head=only_head) != COORDINATES_NOT_FOUND
    return collision_found


def handle_snake_movement(
    state_instance: state.State,
    movement_key: int,
    local_communication_state: state.TransmittedState,
    remote_communication_state: state.TransmittedState,
) -> bool:
    """
    Handles the movement of the snake based on the current state and movement key.

    Args:
        state_instance (state.State): The current game state.
        movement_key (int): The key indicating the new direction of movement.
        local_communication_state (state.TransmittedState): The local communication state.
        remote_communication_state (state.TransmittedState): The remote communication state.

    Returns:
        bool: True if the movement was successful, False otherwise.
    """
    if game_clock.moves():
        state_instance.previous_snake_placement = state_instance.local_snake_placement
        (state_instance.local_snake_placement,
         state_instance.movement_direction, movement_successful) = move_snake(
             state_instance.local_snake_placement,
             state_instance.movement_direction,
             movement_key,
             add_to_snake=state_instance.add_do_snake,
         )
        if not movement_successful:
            return False
        state_instance.food_placement, state_instance.add_do_snake = handle_food_collision(
            state_instance.local_snake_placement,
            state_instance.food_placement,
        )
        add_to_remote_snake = False
        if state_instance.multiplayer and state.is_host(
                local_communication_state, remote_communication_state):
            state_instance.food_placement, add_to_remote_snake = handle_food_collision(
                state_instance.remote_snake_placement,
                state_instance.food_placement,
            )
        if state_instance.multiplayer and (
                state_instance.add_do_snake
                or add_to_remote_snake) and state.is_host(
                    local_communication_state, remote_communication_state):
            food_placed = place_food(
                state_instance.food_placement,
                _combine_bodies_on_grid(
                    state_instance.local_snake_placement,
                    state_instance.remote_snake_placement,
                ))
            if not food_placed:
                return False
        elif not state_instance.multiplayer and state_instance.add_do_snake:
            food_placed = place_food(
                state_instance.food_placement,
                state_instance.local_snake_placement,
            )
            if not food_placed:
                return False
    return True


def _search_collision(placement1: state_types.OBJECT_ND_ARRAY,
                      placement2: state_types.OBJECT_ND_ARRAY,
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
    snake_placement: state_types.OBJECT_ND_ARRAY
) -> state_types.OBJECT_ND_ARRAY:
    initial_shape = snake_placement.shape
    snake_placement = np.array([
        _increment_place(place) if place != state.VOID_PLACE else place
        for row in snake_placement for place in row
    ]).reshape(initial_shape)
    return snake_placement


def _move_head(
    snake_placement: state_types.OBJECT_ND_ARRAY,
    snake_head_coords: tuple[int, int],
    movement_vector: tuple[int,
                           int]) -> tuple[state_types.OBJECT_ND_ARRAY, bool]:
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


def _combine_bodies_on_grid(
    grid_1: state_types.OBJECT_ND_ARRAY,
    grid_2: state_types.OBJECT_ND_ARRAY,
) -> state_types.OBJECT_ND_ARRAY:
    shape = grid_1.shape
    combined_grid = np.full(shape, state.VOID_PLACE, dtype=np.object_)
    for i, rows in enumerate(zip(grid_1, grid_2)):
        row1, row2 = rows
        for k, cols in enumerate(zip(row1, row2)):
            col1, col2 = cols
            is_body = col1[0] in state.SNAKE_PLACES or col2[
                0] in state.SNAKE_BODY_PLACE
            combined_grid[
                i,
                k,
            ] = f"{state.SNAKE_BODY_PLACE}0" if is_body else state.VOID_PLACE
    return combined_grid
