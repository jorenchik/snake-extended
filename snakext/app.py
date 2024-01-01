""" Main loop that triggers the changes in the game """
import asyncio
import threading
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
    game_thread = threading.Thread(
        target=game.run_game,
        args=[
            state.local_transmitted_state_instance,
            state.remote_transmitted_state_instance,
            game_future,
        ],
    )
    game_thread.start()
    loop = asyncio.get_event_loop()
    if arg_parser.MULTIPLAYER:
        try:
            start_server = make_server_task(
                game_future,
                local_transmitted_state_instance,
            )
        except ValueError as e:
            print(e)
            exit(1)
        try:
            start_client = client_client_task(
                game_future,
                local_transmitted_state_instance,
                remote_transmitted_state_instance,
            )
        except ValueError as e:
            print(e)
            exit(1)
        loop.create_task(start_server)
        loop.create_task(start_client)
    asyncio.get_event_loop().run_until_complete(game_future)


def make_server_task(
    future: asyncio.Future[int],
    local_transmitted_state_instance: state.TransmittedState,
) -> Coroutine[Any, Any, websockets.WebSocketServer]:
    if not state.local_transmitted_state_instance:
        raise ValueError("Local communication state is not initialized")
    start_server = communicator.start_server(
        local_transmitted_state=local_transmitted_state_instance,
        future=future)
    return start_server


def client_client_task(
    future: asyncio.Future[int],
    local_transmitted_state_instance: state.TransmittedState,
    remote_transmitted_state_instance: state.TransmittedState,
) -> Coroutine[Any, Any, None]:
    if not state.local_transmitted_state_instance:
        raise ValueError("Local communication state is not initialized")
    if not state.remote_transmitted_state_instance:
        raise ValueError("Remote communication state is not initialized")
    start_client = communicator.start_client(
        remote_transmitted_state=remote_transmitted_state_instance,
        local_transmitted_state=local_transmitted_state_instance,
        future=future)
    return start_client


if __name__ == "__main__":
    main()
