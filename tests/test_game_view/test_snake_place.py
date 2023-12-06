import unittest
from unittest.mock import Mock
import numpy
import numpy.typing as npt
from snakext.utils import pygame_facade
from snakext.views.game_view import _place_snake

SNAKE_BODY = 'b'
SNAKE_HEAD = 'h'
SNAKE_TAIL = 't'


class TestPlaceSnake(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

        b = SNAKE_BODY
        h = SNAKE_HEAD
        t = SNAKE_TAIL
        self.snake_placement = numpy.empty((4, 4), dtype=numpy.str_)
        self.snake_placement[0] = numpy.array(['v' for x in range(0, 4)])
        self.snake_placement[1] = numpy.array(['v', t, b, h])
        self.snake_placement[2] = numpy.array(['v' for x in range(0, 4)])
        self.snake_placement[3] = numpy.array(['v' for x in range(0, 4)])
        self.grid: npt.NDArray[Mock] = numpy.empty((4, 4), dtype=Mock)
        for i in range(0, 4):
            for j in range(0, 4):
                self.grid[i, j] = Mock()
        # self.grid[0] = numpy.array([Mock() for x in range(0, 4)])

    def test_draws_tail_at_the_edge(self):
        _place_snake(self.snake_placement, self.grid)
        self.grid[1][1].draw.assert_called_once()
        self.grid[1][2].draw.assert_called_once()
        self.grid[1][3].draw.assert_called_once()
