import asyncio
from snakext.facades import pygame_facade
from snakext.utils import game_clock
from snakext.game.logic import logic_controller
from snakext.game.state import state
from snakext.game.views import game_view


def init_game() -> None:
    pygame_facade.init_game()
    game_view.init_game_view()
    playground_instance = game_view.playground_instance
    state_instance = state.init_state(
        playground_instance.grid_rows,
        playground_instance.grid_cols,
    )
    state_instance.local_snake_placement = logic_controller.place_initial_snake(
        state_instance.local_snake_placement, )
    state_instance.previous_snake_placement = state_instance.local_snake_placement
    state_instance.food_placement = logic_controller.place_food(
        state_instance.food_placement,
        state_instance.local_snake_placement,
    )
    asyncio.run(_main_game_loop(playground_instance, state_instance))


async def _main_game_loop(playground_instance: game_view.playground.Playground,
                          state_instance: state.State) -> None:
    movement_key = state.RIGHT_DIRECTION
    while True:
        pygame_facade.handle_exit_event()
        game_clock.tick(pygame_facade)
        current_movement_keys = pygame_facade.movement_keys()
        _draw_game_view(playground_instance, state_instance)
        movement_key = pygame_facade.movement_key(
            current_movement_keys,
            pygame_facade.movement_keys,
            movement_key,
        )
        if not _handle_logic_tick(
                playground_instance,
                state_instance,
                movement_key,
        ):
            break
        pygame_facade.pump()


def _handle_logic_tick(
    playground_instance: game_view.playground.Playground,
    state_instance: state.State,
    movement_key: int,
) -> bool:
    if game_clock.is_logic_tick(pygame_facade):
        moved_successfully = _move_snake(state_instance, movement_key)
        if not moved_successfully:
            return False
        game_clock.logic_tick(pygame_facade)
    return True


def _draw_game_view(
    playground_instance: game_view.playground.Playground,
    state_instance: state.State,
) -> None:
    game_view.draw_game_view(
        playground_instance,
        state_instance.local_snake_placement,
        state_instance.food_placement,
    )


def _move_snake(
    state_instance: state.State,
    movement_key: int,
) -> bool:
    if game_clock.moves():
        state_instance.previous_snake_placement = state_instance.local_snake_placement
        state_instance.local_snake_placement, state_instance.movement_direction, movement_successful = logic_controller.move_snake(
            state_instance.local_snake_placement,
            state_instance.movement_direction,
            movement_key,
            add_to_snake=state_instance.add_do_snake,
        )
        if not movement_successful:
            return False
        state_instance.food_placement, state_instance.add_do_snake = logic_controller.handle_food_collision(
            state_instance.local_snake_placement,
            state_instance.food_placement,
        )
        if state_instance.add_do_snake:
            logic_controller.place_food(
                state_instance.food_placement,
                state_instance.local_snake_placement,
            )
    return True
