""" Contains all the state of the game. """

from __future__ import annotations
import numpy as np
import numpy.typing as npt


# TODO inherit from Subject ABC
class State:
    local_state_matrix: npt.NDArray[np.str_]
    remote_state_matrix: npt.NDArray[np.str_]

    # TODO: make Observer ABC
    observers: list[object]

    def __construct__(self, local_state_matrix: npt.NDArray[np.str_],
                      remote_state_matrix: npt.NDArray[np.str_]) -> None:
        self.local_state_matrix = local_state_matrix
        self.remote_state_matrix = remote_state_matrix

    def attach(self, observer: object) -> None:
        pass

    def detach(self, observer: object) -> None:
        pass

    def notify_observers(self) -> None:
        pass


# Global state object
instance = State()
