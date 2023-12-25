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
    if arg_parser.IS_HOST:
        snake_choose_function = matrix.middle_left_element_position
    else:
        snake_choose_function = matrix.middle_right_element_position
    state_instance.local_snake_placement = logic_controller.place_initial_snake(
        state_instance.local_snake_placement,
        choose_coordinates=snake_choose_function,
    )
    state_instance.previous_snake_placement = state_instance.local_snake_placement
    state_instance.food_placement = logic_controller.place_food(
        state_instance.food_placement,
        state_instance.local_snake_placement,
    )
    return playground_instance, state_instance


def run_game(
    local_communication_state: state.TransmittedState,
    remote_communication_state: state.TransmittedState,
    future: asyncio.Future[int],
) -> None:
    playground_instance, state.state_instance = init_game()
    asyncio.run(
        _main_game_loop(
            playground_instance=playground_instance,
            state_instance=state.state_instance,
            local_communication_state=local_communication_state,
            remote_communication_state=remote_communication_state,
            future=future,
        ))
    if not future.done():
        future.set_result(0)


async def _main_game_loop(
    playground_instance: game_view.playground.Playground,
    state_instance: state.State,
    local_communication_state: state.TransmittedState,
    remote_communication_state: state.TransmittedState,
    future: asyncio.Future[int],
) -> None:
    movement_key = state.RIGHT_DIRECTION
    while True:
        game_clock.tick(pygame_facade)
        pygame_facade.handle_exit_event()
        current_movement_keys = pygame_facade.movement_keys()
        local_communication_state.snake_placement = logic_controller.placement_array(
            state_instance.local_snake_placement, )
        state_instance.remote_snake_placement = logic_controller.placement_from_array(
            remote_communication_state.snake_placement,
            (playground_instance.grid_rows, playground_instance.grid_cols),
        )
        _draw_game_view(playground_instance, state_instance)
        movement_key = pygame_facade.movement_key(
            current_movement_keys,
            pygame_facade.movement_keys,
            movement_key,
        )
        if (remote_communication_state.time_last_communicated != 0.0
                and local_communication_state.time_last_communicated != 0.0):
            if game_clock.is_logic_tick(pygame_facade):
                moved_successfully = logic_controller.handle_snake_movement(
                    state_instance, movement_key)
                if not moved_successfully:
                    break
                game_clock.logic_tick(pygame_facade)
        if future.done():
            break
        if logic_controller.check_remote_snake_collision(
                state_instance.local_snake_placement,
                state_instance.remote_snake_placement):
            local_communication_state.stop = True
        pygame_facade.pump()


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
