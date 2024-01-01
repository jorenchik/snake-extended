""" Communicates with other peer for multiplayer. """
import websockets
import asyncio
import time
import json
from typing import Awaitable, Callable, Coroutine, Any
from snakext.game.state import state
from snakext.utils import arg_parser

CONNECTED_MESSAGE = "Connection successful!"
NOT_CONNECTED_MESSAGE = "Connection failed. Trying again..."

PINGS_PER_SECOND = 10
PING_PERIOD = 1 / PINGS_PER_SECOND
PING_WAIT_PERIOD = 0.02
CONNECTION_ATTEMPT_PERIOD = 1

handshake_sent = False
time_received_handshake = 0

current_time = 0.0
local_ping_count = 0
remote_ping_count = 0


def make_server_task(
    future: asyncio.Future[int],
    local_transmitted_state_instance: state.TransmittedState,
) -> Coroutine[Any, Any, websockets.WebSocketServer]:
    if not state.local_transmitted_state_instance:
        raise ValueError("Local communication state is not initialized")
    start_server_task = _start_server(
        local_transmitted_state=local_transmitted_state_instance,
        future=future)
    return start_server_task


def make_client_task(
    future: asyncio.Future[int],
    local_transmitted_state_instance: state.TransmittedState,
    remote_transmitted_state_instance: state.TransmittedState,
) -> Coroutine[Any, Any, None]:
    if not state.local_transmitted_state_instance:
        raise ValueError("Local communication state is not initialized")
    if not state.remote_transmitted_state_instance:
        raise ValueError("Remote communication state is not initialized")
    start_client_task = _start_client(
        remote_transmitted_state=remote_transmitted_state_instance,
        local_transmitted_state=local_transmitted_state_instance,
        future=future)
    return start_client_task


async def _start_client(
    remote_transmitted_state: state.TransmittedState,
    local_transmitted_state: state.TransmittedState,
    future: asyncio.Future[int],
) -> None:
    return await _receive_state(remote_transmitted_state,
                                local_transmitted_state, future)


async def _start_server(
    local_transmitted_state: state.TransmittedState,
    future: asyncio.Future[int],
) -> websockets.WebSocketServer:
    _handle_request = _create_request_handler(local_transmitted_state, future)
    start_server = await websockets.serve(
        _handle_request,
        arg_parser.REMOTE_SERVER_IP,
        arg_parser.LOCAL_SERVER_PORT,
    )
    return start_server


async def _receive_state(
    remote_state: state.TransmittedState,
    local_state: state.TransmittedState,
    future: asyncio.Future[int],
) -> None:
    while True:
        await asyncio.sleep(CONNECTION_ATTEMPT_PERIOD)
        try:
            async with websockets.connect(
                    f"ws://{arg_parser.REMOTE_SERVER_IP}:{arg_parser.REMOTE_SERVER_PORT}"
            ) as websocket:
                print(CONNECTED_MESSAGE)
                await _communicate_remote_state(
                    websocket,
                    remote_state,
                    local_state,
                    future,
                )
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
    global remote_ping_count, handshake_sent
    async for message in websocket:
        local_transmission_state.time_sent = time.time()
        local_transmission_state.is_handshake = True if not handshake_sent else False
        response = json.dumps(local_transmission_state.to_json())
        remote_ping_count += 1
        await websocket.send(response)
        if not handshake_sent:
            handshake_sent = True
            local_transmission_state.sent_handshake = time.time()
        local_transmission_state.time_last_communicated = time.time()
        if future.done():
            await websocket.close_connection()
            return
        if local_transmission_state.game_state == state.GameStates.STOPPED.value:
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
    remote_state: state.TransmittedState,
    local_state: state.TransmittedState,
) -> state.TransmittedState:
    initial_load = json.loads(response)
    received_remote_state = state.TransmittedState.from_json(initial_load)
    remote_state.snake_placement = received_remote_state.snake_placement
    remote_state.food_placement = received_remote_state.food_placement
    remote_state.sent_handshake = received_remote_state.sent_handshake
    remote_state.time_last_communicated = time.time()
    return received_remote_state


async def _communicate_remote_state(
    websocket: websockets.WebSocketClientProtocol,
    remote_state: state.TransmittedState,
    local_state: state.TransmittedState,
    future: asyncio.Future[int],
) -> None:
    global current_time, local_ping_count
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
        received_remote_state = _update_remote_state(
            response,
            remote_state,
            local_state,
        )
        if received_remote_state.game_state == state.GameStates.STOPPED.value:
            future.set_result(0)
            await websocket.close_connection()
            break
