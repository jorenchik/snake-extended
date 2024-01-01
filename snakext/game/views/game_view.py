""" Represents the change of the state. """
from types import ModuleType
from snakext.facades import pygame_facade
from snakext.game.state import state_types
from snakext.game.views import playground
from snakext.game.state import state


def draw_game_view(
    playground: playground.Playground,
    snake_placement: state_types.OBJECT_ND_ARRAY,
    remote_snake_placement: state_types.OBJECT_ND_ARRAY,
    food_placement: state_types.OBJECT_ND_ARRAY,
) -> None:
    _draw_contents(playground, snake_placement, food_placement,
                   remote_snake_placement)
    pygame_facade.update_display()


def _draw_contents(
    playground: playground.Playground,
    snake_placement: state_types.OBJECT_ND_ARRAY,
    food_placement: state_types.OBJECT_ND_ARRAY,
    remote_snake_placement: state_types.OBJECT_ND_ARRAY,
) -> None:
    pygame_facade.fill_background_with_color(playground.background_color)
    _draw_walls(playground)
    _place_food(pygame_facade, playground, food_placement,
                playground.food_grid)
    _place_snake(pygame_facade, playground, snake_placement,
                 playground.snake_grid)
    _place_snake(pygame_facade, playground, remote_snake_placement,
                 playground.remote_snake_grid)


def _draw_walls(playground: playground.Playground) -> None:
    for wall in playground.walls:
        pygame_facade.draw_rect(wall, playground.wall_color)


def _draw_grid(playground: playground.Playground) -> None:
    for row in playground.snake_grid:
        for el in row:
            pygame_facade.draw_rect(el, playground.snake_color)


def _place_snake(pygame_facade: ModuleType, playground: playground.Playground,
                 snake_placement: state_types.OBJECT_ND_ARRAY,
                 grid: state_types.OBJECT_ND_ARRAY) -> None:

    for i, row in enumerate(snake_placement):
        for k, place in enumerate(row):
            if not isinstance(grid[i, k], pygame_facade.Rect):
                raise TypeError("Grid should consist of only Rect objects")
            if place[0] in state.SNAKE_PLACES:
                pygame_facade.draw_rect(grid[i, k], playground.snake_color)


def _place_food(pygame_facade: ModuleType, playground: playground.Playground,
                food_placement: state_types.OBJECT_ND_ARRAY,
                grid: state_types.OBJECT_ND_ARRAY) -> None:

    for i, row in enumerate(food_placement):
        for k, place in enumerate(row):
            if not isinstance(grid[i, k], pygame_facade.Rect):
                raise TypeError("Grid should consist of only Rect objects")
            if place == state.FOOD_PLACE:
                pygame_facade.draw_rect(grid[i, k], playground.food_color)
