""" Main loop that triggers the changes in the game """
import asyncio
import threading
from snakext.game import game
from snakext.game.state import state
from snakext.communication import communicator


def main() -> None:
    state.local_transmitted_state_instance = state.init_transmitted_state()
    state.remote_transmitted_state_instance = state.init_transmitted_state()
    game_future = asyncio.Future()
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
    start_server = communicator.start_server(
        local_transmitted_state=state.local_transmitted_state_instance, )
    start_client = communicator.start_client(
        remote_transmitted_state=state.remote_transmitted_state_instance, )
    loop.create_task(start_server)
    loop.create_task(start_client)
    asyncio.get_event_loop().run_until_complete(game_future)


if __name__ == "__main__":
    main()
