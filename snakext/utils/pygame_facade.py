""" Offers simpler interface for pygame functionality. """
import pygame

GAME_INITIALIZED_SUCCESSFULLY: int = 5
DEFAULT_RESOLUTION: tuple[int, int] = (1280, 720)
DEFAULT_BACKGROUND_COLOR = (255, 255, 255, 255)
DEFAULT_GENERIC_COLOR = (100, 100, 100, 255)

pygame.init()
_screen: pygame.Surface = pygame.display.set_mode(DEFAULT_RESOLUTION)
_clock: pygame.time.Clock = pygame.time.Clock()

Rect = pygame.Rect
Color = pygame.Color


def rect(pos_vector_top_left: tuple[float, float],
         diagonal_vector: tuple[float, float]) -> pygame.Rect:
    rect_pos_left = pos_vector_top_left[0]
    rect_pos_top = pos_vector_top_left[1]
    rect_width = diagonal_vector[0]
    rect_height = diagonal_vector[1]
    return pygame.Rect(rect_pos_left, rect_pos_top, rect_width, rect_height)


def draw_rect(
    rect: pygame.Rect,
    color: pygame.Color,
) -> None:
    pygame.draw.rect(_screen, color, rect)


def fill_background_with_color(background_color: Color) -> None:
    _screen.fill(background_color)


def create_color(rgba_values: tuple[int, int, int, int]) -> Color:
    return Color(rgba_values)


def update_display() -> None:
    pygame.display.flip()


def bottom_screen_pos(bottom: float) -> float:
    return _screen.get_height() - bottom


def right_screen_pos(right: float) -> float:
    return _screen.get_width() - right


def screen_width() -> int:
    return _screen.get_width()


def screen_height() -> int:
    return _screen.get_height()
