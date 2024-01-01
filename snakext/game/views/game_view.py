"""
This module represents the change of state in a snake game by rendering the 
game view. It includes functions to draw the game view, including the snake(s),
food, and walls, using the Pygame facade. The module interacts with the 
playground module for layout and the state module for game state information.
"""
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
    """
    Draws the entire game view including the snake(s), food, and background.

    Args:
        playground (playground.Playground): The playground object with game layout information.
        snake_placement (state_types.OBJECT_ND_ARRAY): The placement array of the local snake.
        remote_snake_placement (state_types.OBJECT_ND_ARRAY): The placement array of the remote snake.
        food_placement (state_types.OBJECT_ND_ARRAY): The placement array of the food.
    """
    _draw_contents(playground, snake_placement, food_placement,
                   remote_snake_placement)
    pygame_facade.update_display()


def _draw_contents(
    playground: playground.Playground,
    snake_placement: state_types.OBJECT_ND_ARRAY,
    food_placement: state_types.OBJECT_ND_ARRAY,
    remote_snake_placement: state_types.OBJECT_ND_ARRAY,
) -> None:
    """
    Helper function to draw the contents of the game.

    Args:
        playground (playground.Playground): The playground object with game layout information.
        snake_placement (state_types.OBJECT_ND_ARRAY): The placement array of the local snake.
        food_placement (state_types.OBJECT_ND_ARRAY): The placement array of the food.
        remote_snake_placement (state_types.OBJECT_ND_ARRAY): The placement array of the remote snake.
    """
    pygame_facade.fill_background_with_color(playground.background_color)
    _draw_walls(playground)
    _place_food(pygame_facade, playground, food_placement,
                playground.food_grid)
    _place_snake(
        pygame_facade,
        playground,
        snake_placement,
        playground.snake_grid,
        playground.local_snake_color,
    )
    _place_snake(
        pygame_facade,
        playground,
        remote_snake_placement,
        playground.remote_snake_grid,
        playground.remote_snake_color,
    )


def _draw_walls(playground_instance: playground.Playground) -> None:
    """
    Draws the walls of the playground.

    Args:
        playground (playground.Playground): The playground object with wall information.
    """
    for wall in playground_instance.walls:
        pygame_facade.draw_rect(
            wall,
            playground_instance.wall_color,
            border_radius=playground.WALL_BORDER_RADIUS,
        )


def _draw_grid(playground: playground.Playground) -> None:
    """
    Draws the grid on the playground.

    Args:
        playground (playground.Playground): The playground object with grid information.
    """
    for row in playground.snake_grid:
        for el in row:
            pygame_facade.draw_rect(el, playground.local_snake_color)


def _place_snake(
    pygame_facade: ModuleType,
    playground: playground.Playground,
    snake_placement: state_types.OBJECT_ND_ARRAY,
    grid: state_types.OBJECT_ND_ARRAY,
    snake_color: pygame_facade.Color,
) -> None:
    """
    Places the snake on the game grid.

    Args:
        pygame_facade (ModuleType): The Pygame facade module for drawing.
        playground (playground.Playground): The playground object with layout information.
        snake_placement (state_types.OBJECT_ND_ARRAY): The placement array of the snake.
        grid (state_types.OBJECT_ND_ARRAY): The grid array to place the snake on.
        snake_color (pygame_facade.Color): Color of the snake drawn

    Raises:
        TypeError: If the grid does not consist of Pygame Rect objects.
    """
    for i, row in enumerate(snake_placement):
        for k, place in enumerate(row):
            if not isinstance(grid[i, k], pygame_facade.Rect):
                raise TypeError("Grid should consist of only Rect objects")
            if place[0] in state.SNAKE_PLACES:
                pygame_facade.draw_rect(grid[i, k], snake_color)


def _place_food(pygame_facade: ModuleType,
                playground_instance: playground.Playground,
                food_placement: state_types.OBJECT_ND_ARRAY,
                grid: state_types.OBJECT_ND_ARRAY) -> None:
    """
    Places the food on the game grid.

    Args:
        pygame_facade (ModuleType): The Pygame facade module for drawing.
        playground (playground.Playground): The playground object with layout information.
        food_placement (state_types.OBJECT_ND_ARRAY): The placement array of the food.
        grid (state_types.OBJECT_ND_ARRAY): The grid array to place the food on.

    Raises:
        TypeError: If the grid does not consist of Pygame Rect objects.
    """
    for i, row in enumerate(food_placement):
        for k, place in enumerate(row):
            if not isinstance(grid[i, k], pygame_facade.Rect):
                raise TypeError("Grid should consist of only Rect objects")
            if place == state.FOOD_PLACE:
                pygame_facade.draw_rect(
                    grid[i, k],
                    playground_instance.food_color,
                    border_radius=playground.FOOD_BORDER_RADIUS,
                )
