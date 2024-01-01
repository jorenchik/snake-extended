""" Main loop that triggers the changes in the game """
import asyncio
import websockets
from typing import Coroutine, Any
from snakext.game import game
from snakext.game.state import state
from snakext.utils import arg_parser
from snakext.communication import communicator


def main() -> None:
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


def _get_server_task(
    game_future: asyncio.Future[int],
    local_transmitted_state: state.TransmittedState,
) -> Coroutine[Any, Any, websockets.WebSocketServer]:
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
