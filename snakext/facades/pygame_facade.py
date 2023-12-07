""" Offers simpler interface for pygame functionality. """
import pygame
from types import ModuleType
from typing import Callable
from snakext.state import state

GAME_INITIALIZED_SUCCESSFULLY: int = 5
DEFAULT_RESOLUTION: tuple[int, int] = (1280, 720)
DEFAULT_BACKGROUND_COLOR = (255, 255, 255, 255)
DEFAULT_GENERIC_COLOR = (100, 100, 100, 255)

_pygame_module: ModuleType
_screen: pygame.Surface | None = None
_clock: pygame.time.Clock | None = None

K_UP = pygame.K_UP
K_RIGHT = pygame.K_RIGHT
K_DOWN = pygame.K_DOWN
K_LEFT = pygame.K_LEFT
MOVEMENT_KEYS = [K_UP, K_RIGHT, K_DOWN, K_LEFT]
KEY_DIRECTION = {
    K_UP: state.TOP_DIRECTION,
    K_RIGHT: state.RIGHT_DIRECTION,
    K_DOWN: state.BOTTOM_DIRECTION,
    K_LEFT: state.LEFT_DIRECTION,
}


def init_game(pygame_module: ModuleType = pygame) -> None:
    global _screen, _clock, _pygame_module
    pygame_module.init()
    _pygame_module = pygame_module
    _screen = pygame.display.set_mode(DEFAULT_RESOLUTION)
    _clock = pygame.time.Clock()


Rect = pygame.Rect
Color = pygame.Color
error = pygame.error


def movement_direction(previous_movement_keys: list[int],
                       get_keys: Callable[[], list[int]]) -> int:
    pressed_keys = get_keys()
    if len(previous_movement_keys) > 0:
        new_pressed_keys = [
            x for x in pressed_keys if x not in previous_movement_keys
        ]
        pressed_keys = new_pressed_keys if len(
            new_pressed_keys) > 0 else pressed_keys
    first_element = pressed_keys[0] if len(pressed_keys) > 0 else 0
    direction = KEY_DIRECTION[first_element] if first_element != 0 else 0
    return direction


def movement_keys() -> list[int]:
    global MOVEMENT_KEYS
    keys_pressed = _get_keys_pressed()
    movement_keys = [x for x in keys_pressed if x in MOVEMENT_KEYS]
    return movement_keys


def _get_keys_pressed() -> list[int]:
    global _pygame_module
    keys_pressed = []
    for event in _pygame_module.event.get():
        if event.type == pygame.KEYDOWN:
            keys_pressed.append(event.key)
    return keys_pressed


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
