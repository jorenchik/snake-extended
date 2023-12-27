""" Communicates with other peer for multiplayer. """
import websockets
import asyncio
import time
import json
from typing import Awaitable, Callable
from snakext.game.state import state
from snakext.utils import arg_parser

CONNECTED_MESSAGE = "Connection successful!"
NOT_CONNECTED_MESSAGE = "Connection failed. Trying again..."

PINGS_PER_SECOND = 10
PING_PERIOD = 1 / PINGS_PER_SECOND
PING_WAIT_PERIOD = 0.02
CONNECTION_ATTEMPT_PERIOD = 1

current_time = 0.0
local_ping_count = 0
remote_ping_count = 0


async def start_client(
    remote_transmitted_state: state.TransmittedState,
    future: asyncio.Future[int],
) -> None:
    return await _receive_state(remote_transmitted_state, future)


async def start_server(
    local_transmitted_state: state.TransmittedState,
    future: asyncio.Future[int],
) -> websockets.WebSocketServer:
    _handle_request = _create_request_handler(local_transmitted_state, future)
    start_server = await websockets.serve(
        _handle_request,
        "localhost",
        arg_parser.LOCAL_PORT,
    )
    return start_server


async def _receive_state(
    remote_state: state.TransmittedState,
    future: asyncio.Future[int],
) -> None:
    while True:
        await asyncio.sleep(CONNECTION_ATTEMPT_PERIOD)
        try:
            async with websockets.connect(
                    f"ws://localhost:{arg_parser.REMOTE_PORT}") as websocket:
                print(CONNECTED_MESSAGE)
                await _communicate_remote_state(websocket, remote_state,
                                                future)
        except OSError:
            print(NOT_CONNECTED_MESSAGE)


def _create_request_handler(
    transmission_state: state.TransmittedState,
    future: asyncio.Future[int],
) -> Callable[[websockets.WebSocketServerProtocol], Awaitable[None]]:

    async def _handler(websocket: websockets.WebSocketServerProtocol) -> None:
        await _respond_to_message_with_transmission_state(
            websocket, transmission_state, future)

    return _handler


async def _respond_to_message_with_transmission_state(
    websocket: websockets.WebSocketServerProtocol,
    local_transmission_state: state.TransmittedState,
    future: asyncio.Future[int],
) -> None:
    global remote_ping_count
    async for message in websocket:
        if future.done():
            await websocket.close_connection()
            return
        response = json.dumps(local_transmission_state.to_json())
        remote_ping_count += 1
        await websocket.send(response)
        local_transmission_state.time_last_communicated = time.time()
        if local_transmission_state.stop:
            future.set_result(0)
            await websocket.close_connection()
            return


def _is_ping(current_time: float) -> bool:
    time_difference = time.time() - current_time
    if time_difference < PING_PERIOD:
        return False
    else:
        return True


def _register_ping() -> tuple[int, float]:
    global local_ping_count
    global current_time
    local_ping_count += 1
    current_time = time.time()
    return local_ping_count - 1, current_time


def _update_remote_state(
        response: str | bytes,
        remote_state: state.TransmittedState) -> state.TransmittedState:
    initial_load = json.loads(response)
    received_remote_state = state.TransmittedState.from_json(initial_load)
    remote_state.snake_placement = received_remote_state.snake_placement
    remote_state.time_last_communicated = time.time()
    return received_remote_state


async def _communicate_remote_state(
    websocket: websockets.WebSocketClientProtocol,
    remote_state: state.TransmittedState,
    future: asyncio.Future[int],
) -> None:
    global current_time
    global local_ping_count
    while True:
        if future.done():
            await websocket.close_connection()
            return
        if not _is_ping(current_time):
            await asyncio.sleep(PING_WAIT_PERIOD)
        local_ping_count, current_time = _register_ping()
        request = f"""Hello from client #{local_ping_count},
                    time: {current_time}"""
        await websocket.send(request)
        response = await websocket.recv()
        received_remote_state = _update_remote_state(response, remote_state)
        if received_remote_state.stop:
            future.set_result(0)
            await websocket.close_connection()
            break
