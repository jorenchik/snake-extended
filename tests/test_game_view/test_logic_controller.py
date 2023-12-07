from unittest import TestCase
from snakext.logic import logic_controller
import numpy as np


class TestMoveSnake(TestCase):

    def setUp(self) -> None:
        self.snake_placement = np.empty((4, 4), dtype=np.object_)
        for i in range(0, 4):
            self.snake_placement[i] = np.array(['v' for x in range(0, 4)])

    # def test_moves_snake_with_no_input(self) -> None:
    #     self.snake_placement[0] = np.array(['t', 'b', 'h', 'v'])
    #     snake_placement = logic_controller.move_snake(self.snake_placement, 0)
    #     control_array = ['v', 'b', 'h', 't']
    #     check_array = [x for x in snake_placement[0]]
    #     self.assertEqual(check_array, control_array)


class TestGetDirection(TestCase):

    def setUp(self) -> None:
        self.snake_placement = np.empty((4, 4), dtype=np.object_)
        for i in range(0, 4):
            self.snake_placement[i] = np.array(['v' for x in range(0, 4)])
