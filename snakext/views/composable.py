import abc
import pygame
from snakext.utils.pygame_interface import PygameInterface


class Composable(abc.ABC):
    rect: pygame.Rect
    color: pygame.Color
    pygame_interface: PygameInterface

    def draw(self) -> None:
        pass
