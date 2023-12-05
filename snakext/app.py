""" Main loop that triggers the changes in the game """
import asyncio
from snakext.views import game_view


async def main_loop() -> None:
    game_view.init_game()
    while True:
        game_view.draw_view()
        await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main_loop())
