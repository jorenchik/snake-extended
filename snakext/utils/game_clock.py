"""
This module manages the timing and ticks for game logic in a game environment,
using a pygame facade. It provides functionalities to handle the timing of 
game ticks and logic ticks, which are essential for consistent game updates 
and logic processing. The module calculates the time difference between ticks 
and determines if it's time to execute game logic based on predefined intervals.
"""
from types import ModuleType

TICKS_PER_SECOND = 30
TICK_PERIOD_SECONDS = 1 / TICKS_PER_SECOND
TICK_PER_MOVE = 5

_game_tick_time = 0
_logic_ticks = 0


def tick(pygame_facade: ModuleType) -> float:
    """
    Updates the game tick time and returns the time difference since the last tick.

    This function is called to update the game's tick count based on the predefined tick period. It calculates the time difference since the last tick and updates the global game tick time.

    Args:
        pygame_facade (ModuleType): The Pygame facade module for accessing tick-related functions.

    Returns:
        float: The time difference in seconds since the last game tick.
    """
    global _game_tick_time
    pygame_facade.tick()
    current_time = pygame_facade.get_ticks_seconds()
    time_difference = current_time - _game_tick_time
    if time_difference >= TICK_PERIOD_SECONDS:
        _game_tick_time = current_time
    return time_difference


def is_logic_tick(pygame_facade: ModuleType) -> bool:
    """
    Determines whether the current time is appropriate for a logic tick.

    This function checks if the time since the last game tick has reached or exceeded the predefined tick period, indicating that it's time for a logic tick.

    Args:
        pygame_facade (ModuleType): The Pygame facade module for accessing tick-related functions.

    Returns:
        bool: True if it's time for a logic tick, False otherwise.
    """
    global _game_tick_time
    time_since_last_game_tick = pygame_facade.get_ticks_seconds(
    ) - _game_tick_time

    is_tick = time_since_last_game_tick >= TICK_PERIOD_SECONDS
    return is_tick


def logic_tick(pygame_facade: ModuleType) -> None:
    """
    Increments the logic tick count.

    This function should be called to signify that a logic tick has occurred, incrementing the internal logic tick counter.

    Args:
        pygame_facade (ModuleType): The Pygame facade module for accessing tick-related functions.
    """
    global _logic_ticks
    _logic_ticks += 1


def moves() -> bool:
    """
    Increments the logic tick count.

    This function should be called to signify that a logic tick has occurred, incrementing the internal logic tick counter.

    Args:
        pygame_facade (ModuleType): The Pygame facade module for accessing tick-related functions.
    """
    global _logic_ticks
    return _logic_ticks % TICK_PER_MOVE == 0
