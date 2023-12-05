""" Represents the change of the state. """
import numpy as np
import numpy.typing as npt
from snakext.views import playground
from snakext.utils import pygame_facade
from typing import Any

SNAKE_COLUMN_COUNT = 30
PLAYGROUND_MARGIN = 40
WALL_MARGIN = 0
WALL_WIDTH = 25
PLAYGROUND_BACKGROUND_COLOR = (129, 143, 180, 255)
WALL_COLOR = (120, 120, 120, 255)
SNAKE_COLOR = (50, 50, 50, 255)

wall_color = pygame_facade.create_color(WALL_COLOR)
background_color = pygame_facade.create_color(PLAYGROUND_BACKGROUND_COLOR)
snake_color = pygame_facade.create_color(SNAKE_COLOR)
_playground_left = PLAYGROUND_MARGIN
_playground_top = PLAYGROUND_MARGIN
_wall_width = WALL_WIDTH
_playground_position = (_playground_left, _playground_top)
_playground_width = pygame_facade.screen_width() - 2 * _playground_left
_playground_height = pygame_facade.screen_height() - 2 * _playground_top
_playground_dimensions = (_playground_width, _playground_height)
_internal_playground_dimensions = (_playground_width - 2 * WALL_WIDTH,
                                   _playground_height - 2 * WALL_WIDTH)
_internal_playground_position = (_playground_position[0] + WALL_WIDTH,
                                 _playground_position[1] + WALL_WIDTH)
_playground_instance: pygame_facade.Rect | None = None
_walls: list[pygame_facade.Rect] = []
_grid: npt.NDArray[Any] = np.empty((0, 0), dtype=pygame_facade.Rect)


def init_game() -> None:
    global _playground_instance, _walls, _grid
    _playground_instance = playground.make_playground(_playground_position)
    _walls = playground.make_walls(_playground_position,
                                   _playground_dimensions, _wall_width)
    _grid = playground.make_rect_grid(_internal_playground_position,
                                      _internal_playground_dimensions,
                                      SNAKE_COLUMN_COUNT)


def draw_view() -> None:
    _draw_contents()
    pygame_facade.update_display()


def _draw_contents() -> None:
    pygame_facade.fill_background_with_color(background_color)
    _draw_walls()
    _draw_grid()


def _draw_walls() -> None:
    for wall in _walls:
        pygame_facade.draw_rect(wall, wall_color)


def _draw_grid() -> None:
    for row in _grid:
        for el in row:
            pygame_facade.draw_rect(el, snake_color)


def _place_snake(snake_index: int,
                 snake_placement: npt.NDArray[np.str_]) -> None:
    pass
