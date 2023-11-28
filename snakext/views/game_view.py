""" Represents the change of the state. """
import numpy
import numpy.typing as npt


class GameView:
    snake_placements: dict[int, list[npt.NDArray[numpy.str_]]]

    def __init__(self) -> None:
        pass

    def make_playground(self) -> None:
        pass

    def place_snake(self, snake_index: int,
                    snake_placement: npt.NDArray[numpy.str_]) -> None:
        pass
