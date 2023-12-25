""" Communicates with other peer for multiplayer. """
import websockets
import asyncio
import sys
import time
import json
from typing import Awaitable, Callable
from snakext.game.state import state
from snakext.utils import arg_parser

PINGS_PER_SECOND = 10
PING_PERIOD = 1 / PINGS_PER_SECOND

current_time = 0.0
local_ping_count = 0
remote_ping_count = 0


async def recieve_state(remote_state: state.TransmittedState) -> None:
    global current_time
    global local_ping_count
    while True:
        await asyncio.sleep(1)
        try:
            async with websockets.connect(
                    f"ws://localhost:{arg_parser.REMOTE_PORT}") as websocket:
                while True:
                    time_difference = time.time() - current_time
                    if time_difference < PING_PERIOD:
                        await asyncio.sleep(0.02)
                        continue
                    request = f"Hello from client #{local_ping_count}, time: {time.time()}"
                    local_ping_count += 1
                    current_time = time.time()
                    await websocket.send(request)
                    response = await websocket.recv()
                    initial_load = json.loads(response)
                    received_remote_state = state.TransmittedState.from_json(
                        initial_load)
                    remote_state.snake_placement = received_remote_state.snake_placement
                    remote_state.time_last_communicated = time.time()
        except Exception as e:
            print(e)


async def _respond_to_message_with_transmission_state(
    websocket: websockets.WebSocketServerProtocol,
    local_transmission_state: state.TransmittedState,
) -> None:
    global remote_ping_count
    async for message in websocket:
        # response = "resp"
        response = json.dumps(local_transmission_state.to_json())
        remote_ping_count += 1
        await websocket.send(response)
        local_transmission_state.time_last_communicated = time.time()


def _create_request_handler(
    transmission_state: state.TransmittedState
) -> Callable[[websockets.WebSocketServerProtocol], Awaitable[None]]:

    async def _handler(websocket: websockets.WebSocketServerProtocol) -> None:
        await _respond_to_message_with_transmission_state(
            websocket, transmission_state)

    return _handler


async def start_client(remote_transmitted_state: state.TransmittedState):
    return await recieve_state(remote_transmitted_state)


async def start_server(local_transmitted_state: state.TransmittedState):
    _handle_request = _create_request_handler(local_transmitted_state)
    start_server = await websockets.serve(
        _handle_request,
        "localhost",
        arg_parser.LOCAL_PORT,
    )
    return start_server
