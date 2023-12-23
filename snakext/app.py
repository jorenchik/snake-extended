""" Main loop that triggers the changes in the game """
import asyncio
from snakext.views import game_view
from snakext.facades import pygame_facade
from snakext.logic import logic_controller
from snakext.state import state
from snakext.utils import game_clock


async def main_loop() -> None:
    pygame_facade.init_game()
    try:
        game_view.init_game_view()
        playground_instance = game_view.playground_instance
    except pygame_facade.error:
        raise pygame_facade.error
    state.init_state(playground_instance.grid_rows,
                     playground_instance.grid_cols)
    state_instance = state.state_instance
    state_instance.snake_placement = logic_controller.place_initial_snake(
        state_instance.snake_placement)
    movement_keys: list[int] = []

    while True:
        game_clock.tick(pygame_facade)
        game_view.draw_game_view(playground_instance,
                                 state_instance.snake_placement)
        if game_clock.is_logic_tick(pygame_facade):
            if game_clock.moves():
                movement_keys = pygame_facade.movement_keys()
                movement_key = pygame_facade.movement_direction(
                    movement_keys, pygame_facade.movement_keys)
                new_snake_state = logic_controller.move_snake(
                    state_instance.snake_placement,
                    state_instance.movement_direction, movement_key)
                state_instance.snake_placement, state_instance.movement_direction = new_snake_state
            game_clock.add_logic_tick(pygame_facade)
            pygame_facade.pump()


if __name__ == "__main__":
    asyncio.run(main_loop())
