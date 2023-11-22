import websockets
import asyncio
import sys

ARGUMENT_COUNT = 3


async def handle_connection(websocket):
    """Continously listen to the client"""
    remote_adress = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    print(f"Connection from {remote_adress}")
    async for message in websocket:
        print(f"{remote_adress}: message")
        await websocket.send("Hello from server")
    print("Connection closed.")


async def communicate_with_server(socket: str):
    """Continously request from server"""
    print(f"Connecting to {socket}...")
    try:
        async with websockets.connect(f"ws://{socket}") as websocket:
            print(f"Connected to {socket}...")
            while True:
                try:
                    await websocket.send("Hello from client")
                    res = await websocket.recv()
                except websockets.exceptions.ConnectionClosedOK:
                    print("Connection closed by server.")
                    break
                except websockets.exceptions.ConnectionClosedError:
                    print("Connection closed with an error.")
                    break
                print(res)
                await asyncio.sleep(1)
            print("Connection closed")
    except ConnectionRefusedError:
        print("Connection failed...")


async def main():
    # Get working arguments
    argv = sys.argv[1:]
    if len(argv) != ARGUMENT_COUNT:
        print("Wrong usage. Correct: [socket] [serves] [connect]")
        exit(1)
    socket = argv[0]

    # Determine behavior
    serves = True if argv[1] == "1" else False
    connects = True if argv[2] == "1" else False
    if serves and connects:
        print("Cannot serve AND connect")
        exit(0)

    # Serve
    if serves:
        server_ip = socket.split(":")[0]
        server_port = int(socket.split(":")[1])
        async with websockets.serve(handle_connection, server_ip, server_port):
            print(f"Listening on port {server_port}...")
            await asyncio.Future()

    # Connect
    elif connects:
        await communicate_with_server(socket)


if __name__ == "__main__":
    asyncio.run(main())
