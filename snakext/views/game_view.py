""" Represents the change of the state. """
import numpy as np
import numpy.typing as npt
from snakext.views import playground
from snakext.utils import pygame_facade
from typing import Any
import types

SNAKE_COLOR = pygame_facade.Color(50, 50, 50, 255)

playground_instance: playground.Playground


def init_game_view() -> None:
    global playground_instance
    playground_instance = playground.init_playground()


def draw_game_view(playground: playground.Playground) -> None:
    _draw_contents(playground)
    pygame_facade.update_display()


def _draw_contents(playground: playground.Playground) -> None:
    pygame_facade.fill_background_with_color(playground.background_color)
    _draw_walls(playground)
    _draw_grid(playground)


def _draw_walls(playground: playground.Playground) -> None:
    for wall in playground.walls:
        pygame_facade.draw_rect(wall, playground.wall_color)


def _draw_grid(playground: playground.Playground) -> None:
    for row in playground.grid:
        for el in row:
            pygame_facade.draw_rect(el, playground.snake_color)


def _place_snake(pygame_facade: types.ModuleType,
                 playground: playground.Playground,
                 snake_placement: npt.NDArray[np.str_],
                 grid: npt.NDArray[Any]) -> None:
    for i, row in enumerate(snake_placement):
        for k, place in enumerate(row):
            if not isinstance(grid[i, k], pygame_facade.Rect):
                raise TypeError("Grid should consist of only Rect objects")
            if place != 'v':
                pygame_facade.draw_rect(grid[i, k], SNAKE_COLOR)
