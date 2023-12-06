""" Represents the change of the state. """
import numpy as np
import numpy.typing as npt
from snakext.views import playground
from snakext.utils import pygame_facade
from typing import Any
from dataclasses import dataclass

SNAKE_COLUMN_COUNT = 30
PLAYGROUND_MARGIN = 40
WALL_MARGIN = 0
WALL_WIDTH = 25
PLAYGROUND_BACKGROUND_COLOR = (129, 143, 180, 255)
WALL_COLOR = (120, 120, 120, 255)
SNAKE_COLOR = (50, 50, 50, 255)


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


_playground_instance: Playground | None = None


def init_game_view() -> None:
    global _playground_instance
    position = (PLAYGROUND_MARGIN, PLAYGROUND_MARGIN)
    dimensions = (pygame_facade.screen_width() - 2 * position[0],
                  pygame_facade.screen_height() - 2 * position[1])
    internal_playground_dimensions = (dimensions[0] - 2 * WALL_WIDTH,
                                      dimensions[1] - 2 * WALL_WIDTH)
    internal_playground_position = (position[0] + WALL_WIDTH,
                                    position[1] + WALL_WIDTH)
    wall_width = WALL_WIDTH
    _playground_instance = Playground(
        (PLAYGROUND_MARGIN, PLAYGROUND_MARGIN),
        (pygame_facade.screen_width() - 2 * position[0],
         pygame_facade.screen_height() - 2 * position[1]), WALL_WIDTH,
        playground.make_walls(position, dimensions, wall_width),
        (dimensions[0] - 2 * WALL_WIDTH, dimensions[1] - 2 * WALL_WIDTH),
        (position[0] + WALL_WIDTH, position[1] + WALL_WIDTH),
        playground.make_rect_grid(internal_playground_position,
                                  internal_playground_dimensions,
                                  SNAKE_COLUMN_COUNT),
        pygame_facade.create_color(WALL_COLOR),
        pygame_facade.create_color(PLAYGROUND_BACKGROUND_COLOR),
        pygame_facade.create_color(SNAKE_COLOR))


def draw_view(playground: Playground) -> None:
    _draw_contents(playground)
    pygame_facade.update_display()


def _draw_contents(playground: Playground) -> None:
    pygame_facade.fill_background_with_color(playground.background_color)
    _draw_walls(playground)
    _draw_grid(playground)


def _draw_walls(playground: Playground) -> None:
    for wall in playground.walls:
        pygame_facade.draw_rect(wall, playground.wall_color)


def _draw_grid(playground: Playground) -> None:
    for row in playground.grid:
        for el in row:
            pygame_facade.draw_rect(el, playground.snake_color)


def _place_snake(playground: Playground, snake_placement: npt.NDArray[np.str_],
                 grid: npt.NDArray[Any]) -> None:
    for i, row in enumerate(snake_placement):
        for k, place in enumerate(row):
            if place != 'v':
                pygame_facade.draw_rect(grid[i, k], playground.snake_color)
