""" Main loop that triggers the changes in the game """
import asyncio
from snakext.game import game


async def main() -> None:
    await game.init_game()


if __name__ == "__main__":
    asyncio.run(main())
