""" Main loop that triggers the changes in the game """
import asyncio
import threading
from snakext.game import game


def main() -> None:
    game_thread = threading.Thread(target=game.init_game)
    game_thread.start()


if __name__ == "__main__":
    main()
