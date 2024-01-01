"""
Entry point of the program. This module initializes and runs the game, handling 
both local and multiplayer modes. It sets up the game environment, processes 
command-line arguments, and manages the game's asynchronous event loop.
"""
import asyncio
import websockets
from typing import Coroutine, Any
from snakext.game import game
from snakext.game.state import state
from snakext.utils import arg_parser
from snakext.communication import communicator


def main() -> None:
    """
    Main function of the program. It initializes the game environment, parses
    command-line arguments, sets up the game thread, and manages the asyncio event loop.
    In multiplayer mode, it also starts the server and client tasks.
    """
    try:
        arg_parser.parse_arguments()
    except AttributeError as e:
        print(e)
        exit(2)
    local_transmitted_state_instance = state.get_local_transmitted_state()
    remote_transmitted_state_instance = state.get_remote_transmitted_state()
    game_future: asyncio.Future[int] = asyncio.Future()
    game_thread = game.make_game_thread(
        local_transmitted_state_instance,
        remote_transmitted_state_instance,
        game_future,
    )
    game_thread.start()
    loop = asyncio.get_event_loop()
    if arg_parser.MULTIPLAYER:
        start_server = _get_server_task(
            game_future,
            local_transmitted_state_instance,
        )
        start_client = _get_client_task(
            game_future,
            local_transmitted_state_instance,
            remote_transmitted_state_instance,
        )
        loop.create_task(start_server)
        loop.create_task(start_client)
        asyncio.get_event_loop().run_until_complete(game_future)
        _get_server_task


def _get_server_task(
    game_future: asyncio.Future[int],
    local_transmitted_state: state.TransmittedState,
) -> Coroutine[Any, Any, websockets.WebSocketServer]:
     """
    Initializes the server task for the multiplayer game.

    Args:
        game_future (asyncio.Future[int]): A future object for the game's completion status.
        local_transmitted_state (state.TransmittedState): The state object for the local game.

    Returns:
        Coroutine[Any, Any, websockets.WebSocketServer]: A coroutine representing the server task.
    """
    try:
        start_server = communicator.make_server_task(
            game_future,
            local_transmitted_state,
        )
    except ValueError as e:
        print(e)
        exit(1)
    return start_server


def _get_client_task(
    game_future: asyncio.Future[int],
    local_transmitted_state: state.TransmittedState,
    remote_transmitted_state: state.TransmittedState,
) -> Coroutine[Any, Any, None]:
    """
    Initializes the client task for the multiplayer game.

    Args:
        game_future (asyncio.Future[int]): A future object for the game's completion status.
        local_transmitted_state (state.TransmittedState): The state object for the local game.
        remote_transmitted_state (state.TransmittedState): The state object for the remote game.

    Returns:
        Coroutine[Any, Any, None]: A coroutine representing the client task.
    """
    try:
        start_client = communicator.make_client_task(
            game_future,
            local_transmitted_state,
            remote_transmitted_state,
        )
    except ValueError as e:
        print(e)
        exit(1)
    return start_client


if __name__ == "__main__":
    main()
