from snakext.sandbox import test_state
from copy import copy

state = test_state.State.instance()


def foo() -> list[int | float]:
    return copy(state.data)
