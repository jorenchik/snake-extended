from types import ModuleType

TICKS_PER_SECOND = 30
TICK_PERIOD_SECONDS = 1 / TICKS_PER_SECOND
TICK_PER_MOVE = 5

_game_tick_time = 0
_logic_ticks = 0


def tick(pygame_facade: ModuleType) -> float:
    global _game_tick_time
    pygame_facade.tick(TICKS_PER_SECOND)
    _previous_tick_time = _game_tick_time
    _game_tick_time = pygame_facade.get_ticks()
    return _game_tick_time - _previous_tick_time


def is_logic_tick(pygame_facade: ModuleType) -> bool:
    global _game_tick_time
    is_tick = pygame_facade.get_ticks(
    ) - _game_tick_time >= TICK_PERIOD_SECONDS
    return is_tick


def add_logic_tick(pygame_facade: ModuleType) -> None:
    global _logic_ticks
    _logic_ticks += 1


def moves() -> bool:
    global _logic_ticks
    return _logic_ticks % TICK_PER_MOVE == 0
