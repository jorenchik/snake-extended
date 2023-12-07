""" Main loop that triggers the changes in the game """
import asyncio
from snakext.views import game_view
from snakext.utils import pygame_facade


async def main_loop() -> None:
    pygame_facade.init_game()
    try:
        game_view.init_game_view()
        playground_instance = game_view.playground_instance
    except pygame_facade.error:
        raise pygame_facade.error
    except TypeError as e:
        raise e
    while True:
        game_view.draw_game_view(playground_instance)
        await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main_loop())
