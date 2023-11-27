""" Offers simpler interface for pygame functionality. """
from __future__ import annotations
import pygame
import asyncio

GAME_INITIALIZED_SUCCESSFULLY: int = 5
DEFAULT_RESOLUTION: tuple[int, int] = (1280, 720)
DEFAULT_BACKGROUND_COLOR: tuple[int, int, int, int] = (255, 255, 255, 255)


class PygameInterface:
    screen: pygame.Surface
    clock: pygame.time.Clock
    blocks: list[pygame.Rect]
    background_color: pygame.Color

    def __init__(self,
                 resolution: tuple[int, int] = DEFAULT_RESOLUTION) -> None:
        try:
            pygame.init()
            self.screen = pygame.display.set_mode(resolution)
            self.clock = pygame.time.Clock()
        except RuntimeError as e:
            raise e
        self.set_background_color(DEFAULT_BACKGROUND_COLOR)
        self.blocks = []

    def set_background_color(
            self, background_color: tuple[int, int, int, int]) -> None:
        (red, green, blue, alpha) = DEFAULT_BACKGROUND_COLOR
        color = pygame.Color(red, green, blue, alpha)
        self.background_color = color

    def make_block(self) -> pygame.Rect:
        rect = pygame.Rect(0, 0, 100, 100)
        self.blocks.append(rect)
        return rect

    def draw_background(self) -> None:
        self.screen.fill(self.background_color)

    def flip(self) -> None:
        pygame.display.flip()

    def end_of_iteration_update(self) -> None:
        self.draw_background()
        for block in self.blocks:
            pygame.draw.rect(self.screen, pygame.Color(0, 0, 0), block)
        self.flip()


# TODO: Make this run only in debug mode (dotenv)
async def test_run_game_in_loop() -> None:
    pg_interface = PygameInterface()
    pg_interface.make_block()
    while True:
        pg_interface.clock.tick(30)
        pg_interface.end_of_iteration_update()


async def test_run() -> None:
    await test_run_game_in_loop()


if __name__ == "__main__":
    asyncio.run(test_run())
