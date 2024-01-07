""" 
Communicates with other peers for multiplayer in a gaming environment. This module 
contains functions and coroutines for setting up and handling server-client 
communications using WebSockets, enabling real-time interaction in a multiplayer game.
"""
import websockets
import asyncio
import time
import json
from typing import Awaitable, Callable, Coroutine, Any
from snakext.game.state import state
from snakext.utils import arg_parser

CONNECTED_MESSAGE = "Connection successful!"
START_SERVER_SUCCESS = "Server started successfully!"
NOT_CONNECTED_MESSAGE = "Connection failed. Trying again..."
CONNECTION_CLOSED_MESSAGE = "Connection closed. Aborting..."

PINGS_PER_SECOND = 3
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
    """
    Creates a coroutine to start a WebSocket server for the game.

    Args:
        future (asyncio.Future[int]): A future object representing the game's completion.
        local_transmitted_state_instance (state.TransmittedState): The game state to be transmitted locally.

    Returns:
        Coroutine[Any, Any, websockets.WebSocketServer]: A coroutine that, when awaited, starts the WebSocket server.

    Raises:
        ValueError: If the local communication state is not initialized.
    """
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
    """
    Creates a coroutine to start a WebSocket client for the game.

    Args:
        future (asyncio.Future[int]): A future object representing the game's completion.
        local_transmitted_state_instance (state.TransmittedState): The game state to be transmitted locally.
        remote_transmitted_state_instance (state.TransmittedState): The game state to be received from a remote source.

    Returns:
        Coroutine[Any, Any, None]: A coroutine that, when awaited, starts the WebSocket client.

    Raises:
        ValueError: If either the local or remote communication state is not initialized.
    """
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
    """
    Starts the client for real-time communication in the multiplayer game.

    This coroutine continuously attempts to connect to the server and, upon success, 
    engages in communication to exchange game states.

    Args:
        remote_transmitted_state (state.TransmittedState): The state object for the remote game.
        local_transmitted_state (state.TransmittedState): The state object for the local game.
        future (asyncio.Future[int]): A future object representing the game's completion status.

    Returns:
        None
    """
    return await _receive_state(remote_transmitted_state,
                                local_transmitted_state, future)


async def _start_server(
    local_transmitted_state: state.TransmittedState,
    future: asyncio.Future[int],
) -> websockets.WebSocketServer:
    """
    Initializes and starts the WebSocket server for the multiplayer game.

    This coroutine sets up the server to listen for incoming connections and handle requests.

    Args:
        local_transmitted_state (state.TransmittedState): The local game state to be transmitted.
        future (asyncio.Future[int]): A future object representing the game's completion status.

    Returns:
        websockets.WebSocketServer: The WebSocket server instance.
    """
    _handle_request = _create_request_handler(local_transmitted_state, future)
    start_server = await websockets.serve(
        _handle_request,
        arg_parser.LOCAL_SERVER_IP,
        arg_parser.LOCAL_SERVER_PORT,
    )
    print(START_SERVER_SUCCESS)
    return start_server


async def _receive_state(
    remote_state: state.TransmittedState,
    local_state: state.TransmittedState,
    future: asyncio.Future[int],
) -> None:
    """
    Manages the reception of game state updates from the remote client.

    This coroutine is part of the client task, continuously attempting to connect to the server
    and receiving updates on the game state.

    Args:
        remote_state (state.TransmittedState): The remote game state instance.
        local_state (state.TransmittedState): The local game state instance.
        future (asyncio.Future[int]): A future object representing the game's completion status.

    Returns:
        None
    """
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
    """
    Creates a request handler for the WebSocket server to manage incoming connections.

    Args:
        transmission_state (state.TransmittedState): The state object to be transmitted.
        future (asyncio.Future[int]): A future object representing the game's completion status.

    Returns:
        Callable[[websockets.WebSocketServerProtocol], Awaitable[None]]: A function that can handle WebSocket requests.
    """

    async def _handler(websocket: websockets.WebSocketServerProtocol) -> None:
        await _respond_to_message_with_transmission_state(
            websocket, transmission_state, future)

    return _handler


async def _respond_to_message_with_transmission_state(
    websocket: websockets.WebSocketServerProtocol,
    local_transmission_state: state.TransmittedState,
    future: asyncio.Future[int],
) -> None:
    """
    Responds to messages from the client with the current game state.

    This coroutine is called by the server to handle incoming client messages and respond
    with the latest game state.

    Args:
        websocket (websockets.WebSocketServerProtocol): The WebSocket connection object.
        local_transmission_state (state.TransmittedState): The local game state to be transmitted.
        future (asyncio.Future[int]): A future object representing the game's completion status.

    Returns:
        None
    """
    global remote_ping_count, handshake_sent
    async for message in websocket:
        local_transmission_state.time_sent = time.time()
        local_transmission_state.is_handshake = True if not handshake_sent else False
        response = json.dumps(local_transmission_state.to_json())
        remote_ping_count += 1
        if future.done():
            try:
                await websocket.close_connection()
            except websockets.exceptions.ConnectionClosedError:
                pass
            break
        try:
            await websocket.send(response)
        except websockets.exceptions.ConnectionClosedError:
            print(CONNECTION_CLOSED_MESSAGE)
            future.set_result(0)
            break
        # Determines who is the host
        if not handshake_sent:
            handshake_sent = True
            local_transmission_state.sent_handshake = time.time()
        local_transmission_state.time_last_communicated = time.time()
        if local_transmission_state.game_state == state.GameStates.STOPPED.value:
            future.set_result(0)
            await websocket.close_connection()
            return


def _is_ping(current_time: float) -> bool:
    """
    Determines if the current time is suitable for sending a ping.

    This function checks whether the specified interval has passed since the last ping.

    Args:
        current_time (float): The current time.

    Returns:
        bool: True if it's time to send a ping, False otherwise.
    """
    time_difference = time.time() - current_time
    if time_difference < PING_PERIOD:
        return False
    else:
        return True


def _register_ping() -> tuple[int, float]:
    """
    Registers a ping event and updates the current time.

    This function increments the ping count and updates the global current time.

    Returns:
        tuple[int, float]: The updated ping count and the current time.
    """
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
    """
    Calculates the position in the middle-right part of the matrix.

    Args:
        matrix (state_types.OBJECT_ND_ARRAY): The matrix to calculate the position for.

    Returns:
        tuple[int, int]: The middle-right position in the matrix.
    """
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
    """
    Manages the communication of the remote game state with the server.

    This coroutine is part of the client task, handling the sending of requests and 
    processing of responses from the server.

    Args:
        websocket (websockets.WebSocketClientProtocol): The WebSocket connection object.
        remote_state (state.TransmittedState): The remote game state instance.
        local_state (state.TransmittedState): The local game state instance.
        future (asyncio.Future[int]): A future object representing the game's completion status.

    Returns:
        None
    """
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
        try:
            await websocket.send(request)
        except websockets.exceptions.ConnectionClosedError:
            print(CONNECTION_CLOSED_MESSAGE)
            future.set_result(0)
            break
        try:
            response = await websocket.recv()
        except websockets.exceptions.ConnectionClosedError:
            print(CONNECTION_CLOSED_MESSAGE)
            future.set_result(0)
            break
        received_remote_state = _update_remote_state(
            response,
            remote_state,
            local_state,
        )
        if received_remote_state.game_state == state.GameStates.STOPPED.value:
            future.set_result(0)
            await websocket.close_connection()
            break
