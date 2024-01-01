""" Contains all the state of the game. """
from __future__ import annotations
import numpy as np
import dataclasses
import json
from snakext.game.state import state_types
from snakext.utils import arg_parser

VOID_PLACE = 'v'
FOOD_PLACE = 'f'
SNAKE_BODY_PLACE = 'b'
SNAKE_TAIL_PLACE = 't'
SNAKE_HEAD_PLACE = 'h'
SNAKE_PLACES: list[str] = [
    SNAKE_TAIL_PLACE, SNAKE_BODY_PLACE, SNAKE_HEAD_PLACE
]
TOP_DIRECTION = 1
BOTTOM_DIRECTION = 2
RIGHT_DIRECTION = 3
LEFT_DIRECTION = 4


@dataclasses.dataclass
class TransmittedState:
    snake_placement: list[tuple[int, int]]
    time_sent: float
    time_last_communicated: float
    stop: bool
    is_handshake: bool
    received_handshake: float
    sent_handshake: float

    def to_json(self) -> str:
        dict_ = dataclasses.asdict(self)
        jsons = json.dumps(dict_)
        return jsons

    @classmethod
    def from_json(cls, json_str: str) -> TransmittedState:
        dict_ = json.loads(json_str)
        transmitted_state = TransmittedState(**dict_)
        return transmitted_state


@dataclasses.dataclass
class State:
    local_snake_placement: state_types.OBJECT_ND_ARRAY
    remote_snake_placement: state_types.OBJECT_ND_ARRAY
    food_placement: state_types.OBJECT_ND_ARRAY
    movement_direction: int
    previous_snake_placement: state_types.OBJECT_ND_ARRAY
    add_do_snake: bool
    multiplayer: bool
    is_host: bool
    is_handshake_done: bool


state_instance: State | None = None
local_transmitted_state_instance: TransmittedState | None = None
remote_transmitted_state_instance: TransmittedState | None = None


def is_handshake_done(
    local_state: TransmittedState,
    remote_state: TransmittedState,
) -> bool:
    received_handshake: bool = (local_state.sent_handshake != 0.0
                                and remote_state.sent_handshake != 0.0)
    return received_handshake


def is_host(
    local_state: TransmittedState,
    remote_state: TransmittedState,
) -> bool:
    return local_state.sent_handshake > remote_state.sent_handshake


def get_game_state(rows: int, cols: int) -> State:
    global state_instance
    if state_instance is None:
        state_instance = _init_state(rows, cols, arg_parser.MULTIPLAYER)
    return state_instance


def get_local_transmitted_state() -> TransmittedState:
    global local_transmitted_state_instance
    if local_transmitted_state_instance is None:
        local_transmitted_state_instance = _init_transmitted_state()
    return local_transmitted_state_instance


def get_remote_transmitted_state() -> TransmittedState:
    global remote_transmitted_state_instance
    if remote_transmitted_state_instance is None:
        remote_transmitted_state_instance = _init_transmitted_state()
    return remote_transmitted_state_instance


def _init_state(
    grid_rows: int,
    grid_cols: int,
    multiplayer: bool = False,
) -> State:
    global state_instance
    grid_shape = (grid_rows, grid_cols)
    local_snake_placement = np.full(grid_shape, 'v', dtype=np.object_)
    remote_snake_placement = np.full(grid_shape, 'v', dtype=np.object_)
    food_placement = np.full(grid_shape, 'v', dtype=np.object_)
    # Choose some direction for the snake
    state_instance = State(
        local_snake_placement=local_snake_placement,
        remote_snake_placement=remote_snake_placement,
        previous_snake_placement=local_snake_placement,
        add_do_snake=False,
        food_placement=food_placement,
        movement_direction=RIGHT_DIRECTION,
        multiplayer=arg_parser.MULTIPLAYER,
        is_host=False,
        is_handshake_done=False,
    )
    return state_instance


def _init_transmitted_state() -> TransmittedState:
    return TransmittedState(
        snake_placement=[],
        time_sent=0.0,
        time_last_communicated=0.0,
        stop=False,
        is_handshake=False,
        received_handshake=0.0,
        sent_handshake=0.0,
    )
