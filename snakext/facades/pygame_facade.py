"""
This module provides a simplified interface for Pygame functionality, 
offering easy-to-use functions for game development tasks such as 
initializing the game window, handling input, and rendering graphics.
Designed to streamline common Pygame operations, it's particularly 
useful for rapid prototyping and educational purposes.
"""
import pygame
import sys
from types import ModuleType
from typing import Callable
from snakext.game.state import state

GAME_INITIALIZED_SUCCESSFULLY: int = 5
DEFAULT_RESOLUTION: tuple[int, int] = (1280, 720)
DEFAULT_BACKGROUND_COLOR = (255, 255, 255, 255)
DEFAULT_GENERIC_COLOR = (100, 100, 100, 255)

_pygame_module: ModuleType
_screen: pygame.Surface | None = None
_clock: pygame.time.Clock | None = None
_keys_pressed: list[int] = []

clock_type = pygame.time.Clock

K_UP = pygame.K_UP
K_RIGHT = pygame.K_RIGHT
K_DOWN = pygame.K_DOWN
K_LEFT = pygame.K_LEFT
MOVEMENT_KEY_SETS = (
    (K_UP, pygame.K_k),
    (K_RIGHT, pygame.K_l),
    (K_DOWN, pygame.K_j),
    (K_LEFT, pygame.K_h),
)
KEY_DIRECTION = {
    K_UP: state.TOP_DIRECTION,
    K_RIGHT: state.RIGHT_DIRECTION,
    K_DOWN: state.BOTTOM_DIRECTION,
    K_LEFT: state.LEFT_DIRECTION,
    pygame.K_k: state.TOP_DIRECTION,
    pygame.K_l: state.RIGHT_DIRECTION,
    pygame.K_j: state.BOTTOM_DIRECTION,
    pygame.K_h: state.LEFT_DIRECTION,
}

EXIT_KEYS = (pygame.K_q, )


def get_ticks_seconds() -> float:
    """
    Returns the number of seconds since the Pygame library was initialized.
    This is achieved by dividing the number of milliseconds from `pygame.time.get_ticks()`
    by 1000 to convert it to seconds.
    """
    return pygame.time.get_ticks() / 1000


def init_game(pygame_module: ModuleType = pygame) -> None:
    """
    Initializes the game environment using the Pygame library.
    This function sets up the main screen and game clock.

    Args:
        pygame_module (ModuleType, optional): The Pygame module to be used. Defaults to pygame.
    """
    global _screen, _clock, _pygame_module
    pygame_module.init()
    _pygame_module = pygame_module
    _screen = pygame.display.set_mode(
        DEFAULT_RESOLUTION,
        flags=pygame.SCALED | pygame.HIDDEN,
    )
    _clock = pygame.time.Clock()


def show_screen() -> None:
    """
    Displays the game screen with the default resolution.
    This function re-initializes the display mode of the screen.
    """
    global _screen
    _screen = pygame.display.set_mode(DEFAULT_RESOLUTION, )


Rect = pygame.Rect
Color = pygame.Color
error = pygame.error


def movement_key(previous_keys: list[int],
                 get_movement_keys: Callable[[], list[int]],
                 default_movement_key: int) -> int:
    """
    Determines the new movement key based on the previous keys and the current movement keys.
    If no new movement key is detected, returns the default movement key.

    Args:
        previous_keys (list[int]): List of keys previously pressed.
        get_movement_keys (Callable[[], list[int]]): Function to get the current movement keys.
        default_movement_key (int): The default movement key to return if no new key is found.

    Returns:
        int: The new movement key or the default movement key.
    """
    new_movement_key = movement_direction(
        previous_keys,
        get_movement_keys,
        default_movement_key,
    )
    return new_movement_key if new_movement_key != 0 else default_movement_key


def movement_direction(
    previous_movement_keys: list[int],
    get_keys: Callable[[], list[int]],
    default_direction: int,
) -> int:
    """
    Calculates the new movement direction based on the pressed keys.

    Args:
        previous_movement_keys (list[int]): List of previously pressed movement keys.
        get_keys (Callable[[], list[int]]): Function to obtain the currently pressed keys.
        default_direction (int): Default direction to fall back to if no new direction is detected.

    Returns:
        int: The new movement direction key, or the default direction if no change is detected.
    """
    pressed_keys = get_keys()
    # Detect newly pressed key that would change direction
    new_pressed_keys = [
        x for x in pressed_keys if x not in previous_movement_keys
    ]
    first_element = new_pressed_keys[0] if len(new_pressed_keys) > 0 else 0
    direction = KEY_DIRECTION[
        first_element] if first_element != 0 else default_direction
    return direction


def tick(fps: int = 0) -> float:
    """
    Advances the game clock by one tick and returns the time spent per frame in seconds.
    Can also be used to control the frame rate of the game.

    Args:
        fps (int, optional): The desired frame rate (frames per second). Defaults to 0 (unlimited).

    Returns:
        float: The time spent per frame in seconds.
    """
    global _clock
    return _clock.tick(fps) / 1000


def pump() -> None:
    pygame.event.pump()


def movement_keys() -> list[int]:
    global MOVEMENT_KEY_SETS
    keys_pressed = pygame.key.get_pressed()
    movement_keys: list[int] = []
    for key_set in MOVEMENT_KEY_SETS:
        for key in key_set:
            if keys_pressed[key]:
                if key in movement_keys:
                    movement_keys.remove(key)
                else:
                    movement_keys.append(key)

    return movement_keys


def is_quit_key() -> bool:
    # current_mod = pygame.key.get_mods()
    pressed_keys = pygame.key.get_pressed()
    for key in EXIT_KEYS:
        if pressed_keys[key]:
            return True
    return False


def is_quit_event() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return is_quit_key()


def exit() -> None:
    pygame.quit()
    sys.exit()


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
    border_radius: int = 0,
) -> None:
    pygame.draw.rect(_screen, color, rect, border_radius=border_radius)


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
