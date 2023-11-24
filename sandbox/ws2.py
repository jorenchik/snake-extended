import websockets
import pygame
import asyncio
import sys

ARGUMENT_COUNT: int = 3
CLIENT_REQUEST_PERIOD: float = 1
GAME_SCREEN_RESOLUTION: tuple[int, int] = (1280, 720)

request_message: str | bytes = ""
server_instance: websockets.WebSocketServer | None = None
client_instance: websockets.WebSocketClientProtocol | None = None


def parse_ip(socket: str) -> tuple[str, str]:
    server_ip = socket.split(":")[0]
    server_port = socket.split(":")[1]
    return server_ip, server_port


async def handle_connection(
        websocket: websockets.WebSocketServerProtocol) -> None:
    global request_message
    """Continously listen to the client"""
    remote_adress = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    print(f"Connection from {remote_adress}")
    request_i = 0
    async for message in websocket:
        print(f'{remote_adress}{message!r}')
        request_message = message
        await websocket.send("Hello from server")
        request_i += 1
    print("Connection closed.")


async def create_client_connection(
        socket: str) -> websockets.WebSocketClientProtocol | None:
    client: websockets.WebSocketClientProtocol | None
    try:
        client = await websockets.connect(f"ws://{socket}")
    except ConnectionRefusedError:
        client = None
    return client


async def request_from_server(
        client_connection: websockets.WebSocketClientProtocol) -> str | bytes:
    await client_connection.send("Hello from client")
    response = await client_connection.recv()
    return response


async def start_server(server_ip: str,
                       server_port: str) -> websockets.WebSocketServer:
    server_port_num = int(server_port)
    start_server = websockets.serve(handle_connection, server_ip,
                                    server_port_num)
    print(f"Listening on port {server_port}...")
    server_instance = await start_server
    return server_instance


async def main() -> None:
    global server_instance
    global client_instance

    # Get working arguments
    argv = sys.argv[1:]
    if len(argv) != ARGUMENT_COUNT:
        print("Wrong usage. Correct: [socket] [serves] [connect]")
        exit(1)
    socket = argv[0]

    # Show the usage of the app
    if "--help" in argv:
        print("[socket] [serves] [connect]")
        exit(0)

    # Determine program behavior
    should_serve = True if argv[1] == "1" else False
    should_request_from_server = True if argv[2] == "1" else False
    if should_serve and should_request_from_server:
        print("Cannot serve AND connect")
        exit(0)

    # Setup the game
    pygame.init()
    screen = pygame.display.set_mode(GAME_SCREEN_RESOLUTION)
    clock = pygame.time.Clock()

    # Serve
    if should_serve:
        server_ip, server_port = parse_ip(socket)
        server_instance = await start_server(server_ip, server_port)

    tick_i = 0
    running = True
    while running:
        tick_i += 1
        # Game logic mock
        await asyncio.sleep(0.5)

        print(f'tick {tick_i}:{request_message!r}')
        if should_serve and server_instance and not server_instance.is_serving(
        ):
            print("Server stopped...restarting")
            start_server_task = start_server(server_ip, server_port)
            await start_server_task
        elif should_request_from_server:
            if not isinstance(client_instance,
                              websockets.WebSocketClientProtocol
                              ) or not client_instance.open:
                client_instance = await create_client_connection(socket)
                if not client_instance:
                    print("Failed to connect to the server")
                    exit(1)
            res: str | bytes = await request_from_server(client_instance)
            print(res)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                if client_instance:
                    await client_instance.close(0)
                if server_instance:
                    server_instance.close(True)
                exit(0)


if __name__ == "__main__":
    asyncio.run(main())
