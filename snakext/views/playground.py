import numpy as np
import numpy.typing as npt
from snakext.utils import pygame_facade
import math
from typing import Any


def add_2d_vectors(vec_1: tuple[float, float],
                   vec_2: tuple[float, float]) -> tuple[float, float]:
    return (vec_1[0] + vec_2[0], vec_1[1] + vec_2[1])


def make_grid(frame_dimensions: tuple[float, float],
              cols: int) -> tuple[float, float, int]:
    slot_width = frame_dimensions[0] / cols
    closest_row_integer = math.floor(frame_dimensions[1] / slot_width)
    slot_height = frame_dimensions[1] / closest_row_integer
    rows = closest_row_integer
    return (slot_width, slot_height, rows)


def create_rect_grid(position_top_left: tuple[float, float],
                     frame_dimensions: tuple[float, float],
                     cols: int) -> npt.NDArray[Any]:
    (slot_width, slot_height, rows) = make_grid(frame_dimensions, cols)
    rect_dimensions = (slot_width - 1, slot_height - 1)
    element_count = rows * cols
    grid: npt.NDArray[Any] = np.empty((rows, cols), dtype=pygame_facade.Rect)
    for i in range(0, element_count):
        x_pos = i % cols
        y_pos = math.floor(i / cols)
        rect_position = (x_pos * slot_width + 1, y_pos * slot_height + 1)
        rect_position = add_2d_vectors(rect_position, position_top_left)
        grid_element = pygame_facade.rect(rect_position, rect_dimensions)
        grid[y_pos, x_pos] = grid_element
    return grid


def create_playground(
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


def create_walls(playground_position: tuple[float, float],
                 playground_dimensions: tuple[float, float],
                 wall_width: float) -> list[pygame_facade.Rect]:
    walls = [
        create_left_wall(playground_position, playground_dimensions,
                         wall_width),
        create_right_wall(playground_position, playground_dimensions,
                          wall_width),
        create_top_wall(playground_position, playground_dimensions,
                        wall_width),
        create_bottom_wall(playground_position, playground_dimensions,
                           wall_width),
    ]
    return walls


def create_right_wall(playground_position: tuple[float, float],
                      playground_dimensions: tuple[float, float],
                      wall_width: float) -> pygame_facade.Rect:
    position_vector: tuple[float,
                           float] = (playground_dimensions[0] - wall_width, 0)
    position_vector = add_2d_vectors(position_vector, playground_position)
    rect_dimensions = (wall_width, playground_dimensions[1])
    wall_rect = pygame_facade.rect(position_vector, rect_dimensions)
    return wall_rect


def create_top_wall(playground_position: tuple[float, float],
                    playground_dimensions: tuple[float, float],
                    wall_width: float) -> pygame_facade.Rect:
    position_vector: tuple[float, float] = (0, 0)
    rect_dimensions = (playground_dimensions[0], wall_width)
    position_vector = add_2d_vectors(position_vector, playground_position)
    wall_rect = pygame_facade.rect(position_vector, rect_dimensions)
    return wall_rect


def create_left_wall(playground_position: tuple[float, float],
                     playground_dimensions: tuple[float, float],
                     wall_width: float) -> pygame_facade.Rect:
    position_vector: tuple[float, float] = (0, 0)
    rect_dimensions = (wall_width, playground_dimensions[1])
    position_vector = add_2d_vectors(position_vector, playground_position)
    wall_rect = pygame_facade.rect(position_vector, rect_dimensions)
    return wall_rect


def create_bottom_wall(playground_position: tuple[float, float],
                       playground_dimensions: tuple[float, float],
                       wall_width: float) -> pygame_facade.Rect:
    position_vector: tuple[float,
                           float] = (0, playground_dimensions[1] - wall_width)
    rect_dimensions = (playground_dimensions[0] - wall_width, wall_width)
    position_vector = add_2d_vectors(position_vector, playground_position)
    wall_rect = pygame_facade.rect(position_vector, rect_dimensions)
    return wall_rect
