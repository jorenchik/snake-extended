import numpy as np
import numpy.typing as npt
from snakext.utils import pygame_facade
import math
from typing import Any
from types import ModuleType
from dataclasses import dataclass

PLAYGROUND_MARGIN = 40
WALL_MARGIN = 0
WALL_WIDTH = 25
FRAME_MARGIN_X = 5
FRAME_MARGIN_Y = 5

playground_position = (PLAYGROUND_MARGIN, PLAYGROUND_MARGIN)
grid_column_count = 30
plauground_background_color = (129, 143, 180, 255)
wall_color = (120, 120, 120, 255)
snake_color = (50, 50, 50, 255)


@dataclass
class Playground:
    position: tuple[float, float]
    dimensions: tuple[float, float]
    wall_width: int
    walls: list[pygame_facade.Rect]
    internal_playground_dimensions: tuple[float, float]
    internal_playground_position: tuple[float, float]
    grid: npt.NDArray[Any]
    wall_color: pygame_facade.Color
    background_color: pygame_facade.Color
    snake_color: pygame_facade.Color


def init_playground() -> Playground:
    dimensions = _playground_dimensions(pygame_facade, playground_position)
    grid_dimensions = _playground_grid_dimensions(dimensions, WALL_WIDTH)
    grid_position = _playground_grid_position(playground_position)
    try:
        playground_instance = Playground(
            playground_position,
            (pygame_facade.screen_width() - 2 * playground_position[0],
             pygame_facade.screen_height() - 2 * playground_position[1]),
            WALL_WIDTH, make_walls(playground_position, dimensions,
                                   WALL_WIDTH),
            (dimensions[0] - 2 * WALL_WIDTH, dimensions[1] - 2 * WALL_WIDTH),
            (playground_position[0] + WALL_WIDTH,
             playground_position[1] + WALL_WIDTH),
            make_rect_grid(grid_position, grid_dimensions, grid_column_count),
            pygame_facade.create_color(wall_color),
            pygame_facade.create_color(plauground_background_color),
            pygame_facade.create_color(snake_color))
    except pygame_facade.error as e:
        raise e
    except TypeError as e:
        raise TypeError(f"Error while initializing Playground: {e}")
    return playground_instance


def make_rect_grid(position_top_left: tuple[float, float],
                   frame_dimensions: tuple[float, float],
                   cols: int) -> npt.NDArray[Any]:
    (position_top_left,
     frame_dimensions) = _add_margin_to_frame(position_top_left,
                                              frame_dimensions)
    (slot_width, slot_height, rows) = _grid_dimensions(frame_dimensions, cols)
    source_list = _rect_grid_list(rows, cols, (slot_width, slot_height),
                                  position_top_left)
    arr = arr_2d(rows, cols, dtype=pygame_facade.Rect)
    arr = _fill_arr_2d(arr, source_list, rows, cols)
    return arr


def make_walls(playground_position: tuple[float, float],
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
    position_top_left = vec_2d_add(position_top_left,
                                   (FRAME_MARGIN_X, FRAME_MARGIN_Y))
    frame_dimensions = vec_2d_add(frame_dimensions,
                                  (-FRAME_MARGIN_X * 2, -FRAME_MARGIN_Y * 2))
    return (position_top_left, frame_dimensions)


def make_playground_rect(
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


def vec_2d_add(vec_1: tuple[float, float],
               vec_2: tuple[float, float]) -> tuple[float, float]:
    return (vec_1[0] + vec_2[0], vec_1[1] + vec_2[1])


def vec_2d_multiply(vec_1: tuple[float, float],
                    vec_2: tuple[float, float]) -> tuple[float, float]:
    return (vec_1[0] * vec_2[0], vec_1[1] * vec_2[1])


def arr_2d(rows: int, cols: int, dtype: type) -> npt.NDArray[Any]:
    return np.empty((rows, cols), dtype=dtype)


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
    (y_pos, x_pos) = _arr_2d_index(idx, cols)
    rect_position = (x_pos * slot_width + 1, y_pos * slot_height + 1)
    rect_position = vec_2d_add(rect_position, start_position)
    return pygame_facade.rect(
        rect_position,
        rect_dimensions,
    )


def _fill_arr_2d(
    arr: npt.NDArray[Any],
    source_list: list[Any],
    rows: int,
    cols: int,
) -> npt.NDArray[Any]:
    for i in range(0, rows * cols):
        (y_pos, x_pos) = _arr_2d_index(i, cols)
        arr[y_pos, x_pos] = source_list[i]
    return arr


def _arr_2d_index(idx: int, cols: int) -> tuple[int, int]:
    x_pos = idx % cols
    y_pos = math.floor(idx / cols)
    return (y_pos, x_pos)


def _rect_grid_list(
    rows: int,
    cols: int,
    slot_dimensions: tuple[float, float],
    starting_position: tuple[float, float],
) -> list[pygame_facade.Rect]:
    source_list: list[pygame_facade.Rect] = []
    for i in range(0, rows * cols):
        (y_pos, x_pos) = _arr_2d_index(i, cols)
        rect_normal_position = (x_pos, y_pos)
        rect_dimensions = vec_2d_add(slot_dimensions, (-1, -1))
        rect_position = vec_2d_multiply(rect_normal_position, slot_dimensions)
        rect_position = vec_2d_add(rect_position, starting_position)
        rect = pygame_facade.rect(rect_position, rect_dimensions)
        source_list.append(rect)
    return source_list


def _make_right_wall(playground_position: tuple[float, float],
                     playground_dimensions: tuple[float, float],
                     wall_width: float) -> pygame_facade.Rect:
    position_vector: tuple[float,
                           float] = (playground_dimensions[0] - wall_width, 0)
    position_vector = vec_2d_add(position_vector, playground_position)
    rect_dimensions = (wall_width, playground_dimensions[1])
    wall_rect = pygame_facade.rect(position_vector, rect_dimensions)
    return wall_rect


def _make_top_wall(playground_position: tuple[float, float],
                   playground_dimensions: tuple[float, float],
                   wall_width: float) -> pygame_facade.Rect:
    position_vector: tuple[float, float] = (0, 0)
    rect_dimensions = (playground_dimensions[0], wall_width)
    position_vector = vec_2d_add(position_vector, playground_position)
    wall_rect = pygame_facade.rect(position_vector, rect_dimensions)
    return wall_rect


def _make_left_wall(playground_position: tuple[float, float],
                    playground_dimensions: tuple[float, float],
                    wall_width: float) -> pygame_facade.Rect:
    position_vector: tuple[float, float] = (0, 0)
    rect_dimensions = (wall_width, playground_dimensions[1])
    position_vector = vec_2d_add(position_vector, playground_position)
    wall_rect = pygame_facade.rect(position_vector, rect_dimensions)
    return wall_rect


def _make_bottom_wall(playground_position: tuple[float, float],
                      playground_dimensions: tuple[float, float],
                      wall_width: float) -> pygame_facade.Rect:
    position_vector: tuple[float,
                           float] = (0, playground_dimensions[1] - wall_width)
    rect_dimensions = (playground_dimensions[0] - wall_width, wall_width)
    position_vector = vec_2d_add(position_vector, playground_position)
    wall_rect = pygame_facade.rect(position_vector, rect_dimensions)
    return wall_rect
