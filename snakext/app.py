""" Main loop that triggers the changes in the game """
import asyncio
from snakext.views import game_view
from snakext.facades import pygame_facade
from snakext.logic import logic_controller
from snakext.state import state

TICKS_PER_SECOND = 30
TICK_PERIOD_SECONDS = 1 / TICKS_PER_SECOND
TICK_PER_MOVE = 5


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
    previous_tick_time = pygame_facade.get_ticks()
    current_time = previous_tick_time
    ticks = 0
    while True:
        pygame_facade.tick(TICKS_PER_SECOND)
        current_time += previous_tick_time
        game_view.draw_game_view(playground_instance,
                                 state_instance.snake_placement)
        if current_time - previous_tick_time >= TICK_PERIOD_SECONDS:
            ticks += 1
            if ticks % TICK_PER_MOVE == 0:
                movement_keys = pygame_facade.movement_keys()
                movement_key = pygame_facade.movement_direction(
                    movement_keys, pygame_facade.movement_keys)
                new_snake_state = logic_controller.move_snake(
                    state_instance.snake_placement,
                    state_instance.movement_direction, movement_key)
                state_instance.snake_placement, state_instance.movement_direction = new_snake_state
            pygame_facade.pump()
            previous_tick_time = current_time


if __name__ == "__main__":
    asyncio.run(main_loop())
