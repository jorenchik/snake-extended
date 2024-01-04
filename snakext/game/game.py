"""
This module manages the initialization, execution, and main game loop of a
multiplayer snake game. It handles game state setup, player connection, and 
asynchronous game flow, integrating closely with components for game logic,
state management, and rendering. Key functions include game initialization,
thread management, and handling the real-time interaction between local and 
remote players.
"""
import asyncio
import threading
from snakext.facades import pygame_facade
from snakext.utils import matrix, game_clock
from snakext.game.logic import logic_controller
from snakext.game.state import state
from snakext.game.views import game_view, playground


async def init_game(
    local_communication_state: state.TransmittedState,
    remote_communication_state: state.TransmittedState,
) -> tuple[
        playground.Playground,
        state.State,
]:
    """
    Initializes the game environment and sets up the game state.

    This coroutine initializes the game using the pygame facade, sets up the playground,
    establishes a connection for multiplayer games, and handles the initial placement of the snake.

    Args:
        local_communication_state (state.TransmittedState): The state object for local communication.
        remote_communication_state (state.TransmittedState): The state object for remote communication.

    Returns:
        tuple[playground.Playground, state.State]: A tuple containing the playground instance and the game state.
    """
    pygame_facade.init_game()
    playground_instance = playground.get_playground()
    state_instance = state.get_game_state(
        playground_instance.grid_rows,
        playground_instance.grid_cols,
    )
    if state_instance.multiplayer:
        await establish_connection(
            state_instance,
            local_communication_state,
            remote_communication_state,
        )
    await setup_initial_placement(
        state_instance=state_instance,
        local_communication_state=local_communication_state,
        remote_communication_state=remote_communication_state,
    )
    if state_instance.multiplayer and not state.is_host(
            local_communication_state,
            remote_communication_state,
    ):
        snake_choose_function = matrix.middle_right_element_position
    else:
        snake_choose_function = matrix.middle_left_element_position
    state_instance.local_snake_placement = logic_controller.place_initial_snake(
        state_instance.local_snake_placement,
        choose_coordinates=snake_choose_function,
    )
    pygame_facade.show_screen()
    state_instance.game_status = state.GameStates.RUNNING.value
    local_communication_state.game_state = state_instance.game_status
    return playground_instance, state_instance


def make_game_thread(
    local_transmitted_state_instance: state.TransmittedState,
    remote_transmitted_state_instance: state.TransmittedState,
    game_future: asyncio.Future[int],
) -> threading.Thread:
    """
    Creates a thread to run the game loop.

    This function creates a separate thread to handle the game's execution, allowing for asynchronous operations.

    Args:
        local_transmitted_state_instance (state.TransmittedState): The local game state for transmission.
        remote_transmitted_state_instance (state.TransmittedState): The remote game state for transmission.
        game_future (asyncio.Future[int]): A future object to indicate the game's completion status.

    Returns:
        threading.Thread: The thread object for the game loop.
    """
    game_thread = threading.Thread(
        target=run_game,
        args=[
            local_transmitted_state_instance,
            remote_transmitted_state_instance,
            game_future,
        ],
    )
    return game_thread


async def establish_connection(
    state_instance: state.State,
    local_communication_state: state.TransmittedState,
    remote_communication_state: state.TransmittedState,
) -> None:
    """
    Establishes a connection for multiplayer games.

    This coroutine waits until the handshake between local and remote states is complete, indicating
    a successful establishment of the multiplayer connection.

    Args:
        state_instance (state.State): The current game state instance.
        local_communication_state (state.TransmittedState): The state object for local communication.
        remote_communication_state (state.TransmittedState): The state object for remote communication.

    Returns:
        None
    """
    if state_instance.multiplayer:
        while True:
            await asyncio.sleep(0.1)
            if state.is_handshake_done(
                    local_communication_state,
                    remote_communication_state,
            ):
                break


async def setup_initial_placement(
    state_instance: state.State,
    local_communication_state: state.TransmittedState,
    remote_communication_state: state.TransmittedState,
) -> None:
    """
    Sets up the initial placement of game elements.

    This coroutine handles the initial placement of the snake and food in the game, 
    particularly in a multiplayer setting where host and client setups might differ.

    Args:
        state_instance (state.State): The current game state instance.
        local_communication_state (state.TransmittedState): The state object for local communication.
        remote_communication_state (state.TransmittedState): The state object for remote communication.

    Returns:
        None
    """
    state_instance.previous_snake_placement = state_instance.local_snake_placement
    is_host = state.is_host(local_communication_state,
                            remote_communication_state)
    if not state_instance.multiplayer or is_host:
        state_instance.food_placement = logic_controller.place_food(
            state_instance.food_placement,
            logic_controller._combine_bodies_on_grid(
                state_instance.local_snake_placement,
                state_instance.remote_snake_placement,
            ),
        )
        if state_instance.multiplayer:
            local_communication_state.food_placement = logic_controller.placement_array(
                state_instance.food_placement)


def run_game(
    local_communication_state: state.TransmittedState,
    remote_communication_state: state.TransmittedState,
    future: asyncio.Future[int],
) -> None:
    """
    Runs the main game loop.

    This function initializes the game and starts the main game loop. It sets the game state
    to complete when the game ends or an interruption occurs.

    Args:
        local_communication_state (state.TransmittedState): The local game state for transmission.
        remote_communication_state (state.TransmittedState): The remote game state for transmission.
        future (asyncio.Future[int]): A future object to indicate the game's completion status.

    Returns:
        None
    """
    playground_instance, state.state_instance = asyncio.run(
        init_game(
            local_communication_state,
            remote_communication_state,
        ))
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
    """
    The main loop of the game, handling game logic and rendering.

    This coroutine continuously updates the game state, processes player inputs, handles 
    multiplayer synchronization, and renders the game view.

    Args:
        playground_instance (game_view.playground.Playground): The playground instance for the game.
        state_instance (state.State): The current game state instance.
        local_communication_state (state.TransmittedState): The local game state for transmission.
        remote_communication_state (state.TransmittedState): The remote game state for transmission.
        future (asyncio.Future[int]): A future object to indicate the game's completion status.

    Returns:
        None
    """
    movement_key = state.RIGHT_DIRECTION
    while True:
        game_clock.tick(pygame_facade)
        if state_instance.multiplayer and (
                remote_communication_state.game_state
                == state.GameStates.STOPPED.value):
            future.set_result(0)
            break
        if (not state_instance.multiplayer and state_instance.game_status
                == state.GameStates.STOPPED.value):
            future.set_result(0)
            break
        if future.done():
            break

        if pygame_facade.is_quit_event():
            local_communication_state.game_state = state.GameStates.STOPPED.value
            pygame_facade.exit()

        current_movement_keys = pygame_facade.movement_keys()

        if state_instance.multiplayer:
            local_communication_state.snake_placement = logic_controller.placement_array(
                state_instance.local_snake_placement, )
            if state.is_host(local_communication_state,
                             remote_communication_state):
                local_communication_state.food_placement = logic_controller.placement_array(
                    state_instance.food_placement)
            state_instance.remote_snake_placement = logic_controller.placement_from_array(
                remote_communication_state.snake_placement,
                (playground_instance.grid_rows, playground_instance.grid_cols),
                f"{state.SNAKE_BODY_PLACE}0",
            )

        if state_instance.multiplayer and not state.is_host(
                local_communication_state,
                remote_communication_state,
        ):
            state_instance.food_placement = logic_controller.placement_from_array(
                remote_communication_state.food_placement,
                (playground_instance.grid_rows, playground_instance.grid_cols),
                state.FOOD_PLACE,
            )

        _draw_game_view(playground_instance, state_instance)

        movement_key = pygame_facade.movement_key(
            current_movement_keys,
            pygame_facade.movement_keys,
            movement_key,
        )

        if state_instance.game_status == state.GameStates.RUNNING.value:
            if game_clock.is_logic_tick(pygame_facade):
                moved_successfully = logic_controller.handle_snake_movement(
                    state_instance,
                    movement_key,
                    local_communication_state,
                    remote_communication_state,
                )
                if not moved_successfully:
                    state_instance.game_status = state.GameStates.STOPPED.value
                game_clock.logic_tick(pygame_facade)

        if state_instance.multiplayer:
            if logic_controller.check_remote_snake_collision(
                    state_instance.local_snake_placement,
                    state_instance.remote_snake_placement,
            ):
                state_instance.game_status = state.GameStates.STOPPED.value
                local_communication_state.game_state = state_instance.game_status

        pygame_facade.pump()


def _draw_game_view(
    playground_instance: game_view.playground.Playground,
    state_instance: state.State,
) -> None:
    """
    Draws the current state of the game.

    This function is responsible for rendering the game's visual elements, including the snake, food,
    and any other graphical components.

    Args:
        playground_instance (game_view.playground.Playground): The playground instance for the game.
        state_instance (state.State): The current game state instance.

    Returns:
        None
    """
    game_view.draw_game_view(
        playground_instance,
        state_instance.local_snake_placement,
        state_instance.remote_snake_placement,
        state_instance.food_placement,
    )
