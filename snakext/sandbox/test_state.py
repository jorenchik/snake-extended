from __future__ import annotations
from copy import copy

START_DATA: list[int | float] = [2, 3, 4, 5, 6, 7, 8]


class State:
    _instance = None
    data: list[int | float]

    def __init__(self) -> None:
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls) -> State:
        if cls._instance is None:
            print('Creating new instance')
            cls._instance = cls.__new__(cls)
            cls._instance.data = copy(START_DATA)
        return cls._instance
