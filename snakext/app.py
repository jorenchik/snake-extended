""" Main loop that triggers the changes in the game """
import asyncio
from snakext.views import game_view
from snakext.utils import pygame_facade


async def main_loop() -> None:
    pygame_facade.init_game()
    game_view.init_game()
    while True:
        game_view.draw_view(game_view._playground_instance)
        await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main_loop())
