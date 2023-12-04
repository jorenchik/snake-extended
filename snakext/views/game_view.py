""" Represents the change of the state. """
import numpy
import numpy.typing as npt
from snakext.views import playground
from snakext.utils import pygame_facade

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
_playground_instance = playground.create_playground(_playground_position)
_walls = playground.create_walls(_playground_position, _playground_dimensions,
                                 _wall_width)
_grid = playground.create_rect_grid(_internal_playground_position,
                                    _internal_playground_dimensions,
                                    SNAKE_COLUMN_COUNT)


def init_game() -> None:
    pass


def draw_walls() -> None:
    for wall in _walls:
        pygame_facade.draw_rect(wall, wall_color)


def draw_grid() -> None:
    for row in _grid:
        for el in row:
            pygame_facade.draw_rect(el, snake_color)


def draw_view() -> None:
    pygame_facade.fill_background_with_color(background_color)
    draw_walls()
    draw_grid()
    pygame_facade.update_display()


def place_snake(snake_index: int,
                snake_placement: npt.NDArray[numpy.str_]) -> None:
    pass


def draw_contents() -> None:
    pass
