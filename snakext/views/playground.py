import pygame
from snakext.utils.pygame_interface import pygame_interface
from snakext.views.composable import Composable

DEFAULT_PLAYGROUND_WIDTH_FRACTION = 0.7
DEFAULT_PLAYGROUND_HEIGHT_FRACTION = 0.7
DEFAULT_PLAYGROUND_BACKGROUND_COLOR = pygame.Color(129, 143, 180, 255)
DEFAULT_WALL_COLOR = pygame.Color(67, 85, 133, 255)


class Wall(Composable):
    rect: pygame.Rect
    color: pygame.Color

    def __init__(
        self,
        color: pygame.Color = DEFAULT_WALL_COLOR,
    ) -> None:
        self.color = color
        self.rect = pygame.Rect(10, 10, 10, 10)

    def draw(self, surface: pygame.Surface | None = None) -> None:
        pygame_interface.draw_rect(self.rect, surface, self.color)


class PlaygroundBackground(Composable):
    rect: pygame.Rect
    color: pygame.Color

    def __init__(
        self,
        color: pygame.Color = DEFAULT_PLAYGROUND_BACKGROUND_COLOR,
    ) -> None:
        self.color = color
        self.rect = pygame.Rect(10, 10, 10, 10)

    def draw(self, surface: pygame.Surface | None = None) -> None:
        pygame_interface.draw_rect(self.rect, surface, self.color)


class Playground(Composable):
    elements: dict[type[Composable], list[Composable]]

    def __init__(
            self,
            width_fraction: float = DEFAULT_PLAYGROUND_WIDTH_FRACTION,
            height_fraction: float = DEFAULT_PLAYGROUND_HEIGHT_FRACTION
    ) -> None:
        self.rect = pygame.Rect(10, 10, 10, 10)
        self.elements = {}

    def draw(self) -> None:
        for key, val in self.elements.items():
            for rect in val:
                rect.draw()
