from types import ModuleType

TICKS_PER_SECOND = 30
TICK_PERIOD_SECONDS = 1 / TICKS_PER_SECOND
TICK_PER_MOVE = 5

_game_tick_time = 0
_logic_ticks = 0


def tick(pygame_facade: ModuleType) -> float:
    global _game_tick_time
    pygame_facade.tick()
    current_time = pygame_facade.get_ticks_seconds()
    time_difference = current_time - _game_tick_time
    if time_difference >= TICK_PERIOD_SECONDS:
        _game_tick_time = current_time
    return time_difference


def is_logic_tick(pygame_facade: ModuleType) -> bool:
    global _game_tick_time
    time_since_last_game_tick = pygame_facade.get_ticks_seconds(
    ) - _game_tick_time

    is_tick = time_since_last_game_tick >= TICK_PERIOD_SECONDS
    return is_tick


def logic_tick(pygame_facade: ModuleType) -> None:
    global _logic_ticks
    _logic_ticks += 1


def moves() -> bool:
    global _logic_ticks
    return _logic_ticks % TICK_PER_MOVE == 0
