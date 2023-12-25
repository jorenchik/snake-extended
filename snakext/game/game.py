import asyncio
from snakext.facades import pygame_facade
from snakext.utils import game_clock, matrix, arg_parser
from snakext.game.logic import logic_controller
from snakext.game.state import state
from snakext.game.views import game_view, playground


def init_game() -> tuple[
    playground.Playground,
    state.State,
]:
    pygame_facade.init_game()
    game_view.init_game_view()
    playground_instance = game_view.playground_instance
    state_instance = state.init_state(
        playground_instance.grid_rows,
        playground_instance.grid_cols,
    )
    snake_choose_function = matrix.middle_left_element_position if arg_parser.IS_HOST else matrix.middle_right_element_position
    state_instance.local_snake_placement = logic_controller.place_initial_snake(
        state_instance.local_snake_placement,
        choose_coordinates=snake_choose_function,
    )
    state_instance.previous_snake_placement = state_instance.local_snake_placement
    state_instance.food_placement = logic_controller.place_food(
        state_instance.food_placement,
        state_instance.local_snake_placement,
    )
    return (
        playground_instance,
        state_instance,
    )


def run_game(
    local_transmitted_state_instance: state.TransmittedState,
    remote_transmitted_state_instance: state.TransmittedState,
) -> None:
    (
        playground_instance,
        state.state_instance,
    ) = init_game()
    asyncio.run(
        _main_game_loop(
            playground_instance,
            state.state_instance,
            local_transmitted_state_instance,
            remote_transmitted_state_instance,
        ))


async def _main_game_loop(
    playground_instance: game_view.playground.Playground,
    state_instance: state.State,
    local_transmitted_state_instance: state.TransmittedState,
    remote_transmitted_state_instance: state.TransmittedState,
) -> None:
    movement_key = state.RIGHT_DIRECTION
    while True:
        pygame_facade.handle_exit_event()
        game_clock.tick(pygame_facade)
        current_movement_keys = pygame_facade.movement_keys()
        state_instance.remote_snake_placement = logic_controller.placement_from_array(
            remote_transmitted_state_instance.snake_placement,
            (playground_instance.grid_rows, playground_instance.grid_cols),
        )
        _draw_game_view(playground_instance, state_instance)
        movement_key = pygame_facade.movement_key(
            current_movement_keys,
            pygame_facade.movement_keys,
            movement_key,
        )
        if (remote_transmitted_state_instance.time_last_communicated != 0.0 and
                local_transmitted_state_instance.time_last_communicated != 0.0
                and not _handle_logic_tick(
                    playground_instance,
                    state_instance,
                    movement_key,
                    local_transmitted_state_instance,
                    remote_transmitted_state_instance,
                )):
            break

        pygame_facade.pump()


def _handle_logic_tick(
    playground_instance: game_view.playground.Playground,
    state_instance: state.State,
    movement_key: int,
    local_transmitted_state_instance: state.TransmittedState,
    remote_transmitted_state_instance: state.TransmittedState,
) -> bool:
    if game_clock.is_logic_tick(pygame_facade):
        moved_successfully = _move_snake(state_instance, movement_key)
        if not moved_successfully:
            return False
        local_transmitted_state_instance.snake_placement = logic_controller.placement_array(
            state_instance.local_snake_placement, )
        game_clock.logic_tick(pygame_facade)
    return True


def _draw_game_view(
    playground_instance: game_view.playground.Playground,
    state_instance: state.State,
) -> None:
    game_view.draw_game_view(
        playground_instance,
        state_instance.local_snake_placement,
        state_instance.remote_snake_placement,
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
