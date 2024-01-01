"""
This module is responsible for defining and initializing the playground for a 
snake game. It includes the creation of the game area, grid for snake and food 
placement, and the walls. Utilizing Pygame facade for rendering, it calculates 
dimensions and positions for the game elements based on the screen size and 
predefined margins. The module provides functionality to generate a Playground 
instance with all necessary components for the game's visual representation.
"""

import numpy as np
import math
from types import ModuleType
from dataclasses import dataclass
from snakext.facades import pygame_facade
from snakext.utils import matrix, vec
from snakext.game.state import state_types

PLAYGROUND_MARGIN = 40
WALL_MARGIN = 0
WALL_WIDTH = 25
PLAYGROUND_POSITION = (PLAYGROUND_MARGIN, PLAYGROUND_MARGIN)
FRAME_MARGIN_X = 5
FRAME_MARGIN_Y = 5
GRID_COLUMN_COUNT = 30

WALL_COLOR = pygame_facade.Color(120, 120, 120, 255)
SNAKE_COLOR = pygame_facade.Color(50, 50, 50, 255)
FOOD_COLOR = pygame_facade.Color(50, 205, 50, 255)
PLAYGROUND_BACKGROUND_COLOR = pygame_facade.Color(129, 143, 180, 255)


@dataclass
class Playground:
    """
    Represents the playground where the snake game takes place.

    This data class stores the dimensions and positions of various game elements
    such as walls, the snake grid, and food grid. It includes the colors used
    for rendering these elements and manages their arrangement within the game window.
    """
    position: tuple[float, float]
    dimensions: tuple[float, float]
    wall_width: int
    walls: list[pygame_facade.Rect]
    internal_playground_dimensions: tuple[float, float]
    internal_playground_position: tuple[float, float]
    snake_grid: state_types.OBJECT_ND_ARRAY
    remote_snake_grid: state_types.OBJECT_ND_ARRAY
    grid_rows: int
    grid_cols: int
    wall_color: pygame_facade.Color
    background_color: pygame_facade.Color
    snake_color: pygame_facade.Color
    food_grid: state_types.OBJECT_ND_ARRAY
    food_color: pygame_facade.Color


playground_instance: Playground | None = None


def get_playground() -> Playground:
    global playground_instance
    if playground_instance is None:
        playground_instance = _init_playground()
    return playground_instance


def _init_playground() -> Playground:

    dimensions = _playground_dimensions(pygame_facade, PLAYGROUND_POSITION)
    grid_dimensions = _playground_grid_dimensions(dimensions, WALL_WIDTH)
    grid_position = _playground_grid_position(PLAYGROUND_POSITION)
    snake_grid: state_types.OBJECT_ND_ARRAY = _make_rect_grid(
        grid_position, grid_dimensions, GRID_COLUMN_COUNT)
    remote_snake_grid: state_types.OBJECT_ND_ARRAY = _make_rect_grid(
        grid_position, grid_dimensions, GRID_COLUMN_COUNT)
    food_grid: state_types.OBJECT_ND_ARRAY = _make_rect_grid(
        grid_position, grid_dimensions, GRID_COLUMN_COUNT)
    (grid_rows, grid_cols) = snake_grid.shape
    try:
        playground_instance = Playground(
            position=PLAYGROUND_POSITION,
            dimensions=(pygame_facade.screen_width() -
                        2 * PLAYGROUND_POSITION[0],
                        pygame_facade.screen_height() -
                        2 * PLAYGROUND_POSITION[1]),
            wall_width=WALL_WIDTH,
            walls=_make_walls(PLAYGROUND_POSITION, dimensions, WALL_WIDTH),
            internal_playground_dimensions=(dimensions[0] - 2 * WALL_WIDTH,
                                            dimensions[1] - 2 * WALL_WIDTH),
            internal_playground_position=(PLAYGROUND_POSITION[0] + WALL_WIDTH,
                                          PLAYGROUND_POSITION[1] + WALL_WIDTH),
            snake_grid=snake_grid,
            remote_snake_grid=remote_snake_grid,
            grid_rows=grid_rows,
            grid_cols=grid_cols,
            wall_color=pygame_facade.create_color(WALL_COLOR),
            background_color=pygame_facade.create_color(
                PLAYGROUND_BACKGROUND_COLOR),
            snake_color=pygame_facade.create_color(SNAKE_COLOR),
            food_grid=food_grid,
            food_color=pygame_facade.create_color(FOOD_COLOR),
        )
    except pygame_facade.error as e:
        raise e
    except TypeError as e:
        raise TypeError(f"Error while initializing Playground: {e}")
    return playground_instance


def _make_rect_grid(position_top_left: tuple[float, float],
                    frame_dimensions: tuple[float, float],
                    cols: int) -> state_types.OBJECT_ND_ARRAY:
    (position_top_left,
     frame_dimensions) = _add_margin_to_frame(position_top_left,
                                              frame_dimensions)
    (slot_width, slot_height, rows) = _grid_dimensions(frame_dimensions, cols)
    source_list = _rect_grid_list(rows, cols, (slot_width, slot_height),
                                  position_top_left)
    arr = np.empty((rows, cols), dtype=pygame_facade.Rect)
    arr = matrix.fill_matrix(arr, source_list, rows, cols)
    return arr


def _make_walls(playground_position: tuple[float, float],
                playground_dimensions: tuple[float, float],
                wall_width: float) -> list[pygame_facade.Rect]:
    walls = [
        _make_left_wall(playground_position, playground_dimensions,
                        wall_width),
        _make_right_wall(playground_position, playground_dimensions,
                         wall_width),
        _make_top_wall(playground_position, playground_dimensions, wall_width),
        _make_bottom_wall(playground_position, playground_dimensions,
                          wall_width),
    ]
    return walls


def _playground_dimensions(
        pygame_facade: ModuleType,
        playground_position: tuple[float, float]) -> tuple[float, float]:
    return pygame_facade.screen_width() - 2 * playground_position[
        0], pygame_facade.screen_height() - 2 * playground_position[1]


def _playground_grid_dimensions(playground_dimensions: tuple[float, float],
                                wall_width: float) -> tuple[float, float]:
    return playground_dimensions[0] - 2 * WALL_WIDTH, playground_dimensions[
        1] - 2 * WALL_WIDTH


def _playground_grid_position(
        playground_position: tuple[float, float]) -> tuple[float, float]:
    return playground_position[0] + WALL_WIDTH, playground_position[
        1] + WALL_WIDTH


def _add_margin_to_frame(
    position_top_left: tuple[float, float], frame_dimensions: tuple[float,
                                                                    float]
) -> tuple[tuple[float, float], tuple[float, float]]:
    position_top_left = vec.vec_2d_add(position_top_left,
                                       (FRAME_MARGIN_X, FRAME_MARGIN_Y))
    frame_dimensions = vec.vec_2d_add(
        frame_dimensions, (-FRAME_MARGIN_X * 2, -FRAME_MARGIN_Y * 2))
    return (position_top_left, frame_dimensions)


def _make_playground_rect(
        playground_position_top_left: tuple[float,
                                            float]) -> pygame_facade.Rect:
    playground_width = pygame_facade.screen_width(
    ) - 2 * playground_position_top_left[0]
    playground_height = pygame_facade.screen_height(
    ) - 2 * playground_position_top_left[1]
    diagonal_vector = (playground_width, playground_height)
    playground_rect = pygame_facade.rect(playground_position_top_left,
                                         diagonal_vector)
    return playground_rect


def _grid_dimensions(frame_dimensions: tuple[float, float],
                     cols: int) -> tuple[float, float, int]:
    slot_width = frame_dimensions[0] / cols
    closest_row_integer = math.floor(frame_dimensions[1] / slot_width)
    slot_height = frame_dimensions[1] / closest_row_integer
    rows = closest_row_integer
    return (slot_width, slot_height, rows)


def _grid_element(idx: int, rows: int, cols: int, slot_width: float,
                  slot_height: float, start_position: tuple[float, float],
                  rect_dimensions: tuple[float, float]) -> pygame_facade.Rect:
    (y_pos, x_pos) = matrix.matrix_position_of_index(idx, cols)
    rect_position = (x_pos * slot_width + 1, y_pos * slot_height + 1)
    rect_position = vec.vec_2d_add(rect_position, start_position)
    return pygame_facade.rect(
        rect_position,
        rect_dimensions,
    )


def _rect_grid_list(
    rows: int,
    cols: int,
    slot_dimensions: tuple[float, float],
    starting_position: tuple[float, float],
) -> list[pygame_facade.Rect]:
    source_list: list[pygame_facade.Rect] = []
    for i in range(0, rows * cols):
        (y_pos, x_pos) = matrix.matrix_position_of_index(i, cols)
        rect_normal_position = (x_pos, y_pos)
        rect_dimensions = vec.vec_2d_add(slot_dimensions, (-1, -1))
        rect_position = vec.vec_2d_multiply(rect_normal_position,
                                            slot_dimensions)
        rect_position = vec.vec_2d_add(rect_position, starting_position)
        rect = pygame_facade.rect(rect_position, rect_dimensions)
        source_list.append(rect)
    return source_list


def _make_right_wall(playground_position: tuple[float, float],
                     playground_dimensions: tuple[float, float],
                     wall_width: float) -> pygame_facade.Rect:
    position_vector: tuple[float,
                           float] = (playground_dimensions[0] - wall_width, 0)
    position_vector = vec.vec_2d_add(position_vector, playground_position)
    rect_dimensions = (wall_width, playground_dimensions[1])
    wall_rect = pygame_facade.rect(position_vector, rect_dimensions)
    return wall_rect


def _make_top_wall(playground_position: tuple[float, float],
                   playground_dimensions: tuple[float, float],
                   wall_width: float) -> pygame_facade.Rect:
    position_vector: tuple[float, float] = (0, 0)
    rect_dimensions = (playground_dimensions[0], wall_width)
    position_vector = vec.vec_2d_add(position_vector, playground_position)
    wall_rect = pygame_facade.rect(position_vector, rect_dimensions)
    return wall_rect


def _make_left_wall(playground_position: tuple[float, float],
                    playground_dimensions: tuple[float, float],
                    wall_width: float) -> pygame_facade.Rect:
    position_vector: tuple[float, float] = (0, 0)
    rect_dimensions = (wall_width, playground_dimensions[1])
    position_vector = vec.vec_2d_add(position_vector, playground_position)
    wall_rect = pygame_facade.rect(position_vector, rect_dimensions)
    return wall_rect


def _make_bottom_wall(playground_position: tuple[float, float],
                      playground_dimensions: tuple[float, float],
                      wall_width: float) -> pygame_facade.Rect:
    position_vector: tuple[float,
                           float] = (0, playground_dimensions[1] - wall_width)
    rect_dimensions = (playground_dimensions[0] - wall_width, wall_width)
    position_vector = vec.vec_2d_add(position_vector, playground_position)
    wall_rect = pygame_facade.rect(position_vector, rect_dimensions)
    return wall_rect
