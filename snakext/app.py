""" Main loop that triggers the changes in the game """
import asyncio
from snakext.views import game_view
from snakext.facades import pygame_facade
from snakext.logic import logic_controller
from snakext.state import state


async def main_loop() -> None:
    pygame_facade.init_game()
    try:
        game_view.init_game_view()
        playground_instance = game_view.playground_instance
    except pygame_facade.error:
        raise pygame_facade.error
    except TypeError as e:
        raise e
    state.init_state(playground_instance.grid_rows,
                     playground_instance.grid_cols)
    state_instance = state.state_instance
    state_instance.snake_placement = logic_controller.place_initial_snake(
        state_instance.snake_placement)
    movement_keys: list[int] = []
    while True:
        movement_key = pygame_facade.movement_direction(
            movement_keys, pygame_facade.movement_keys)
        state_instance.snake_placement = logic_controller.move_snake(
            state_instance.snake_placement, movement_key)
        game_view.draw_game_view(playground_instance,
                                 state_instance.snake_placement)
        await asyncio.sleep(0.5)
        movement_keys = pygame_facade.movement_keys()


if __name__ == "__main__":
    asyncio.run(main_loop())
