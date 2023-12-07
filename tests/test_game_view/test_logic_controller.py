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

    def test_gets_right_direction(self) -> None:
        self.snake_placement[0] = np.array(['v', 'v', 'v', 'v'])
        self.snake_placement[1] = np.array(['v', 'b2', 'h1', 'v'])
        self.snake_placement[2] = np.array(['v', 'v', 'v', 'v'])
        self.snake_placement[3] = np.array(['v', 'v', 'v', 'v'])
        snake_placement = logic_controller.get_direction(self.snake_placement)
        self.assertEqual(snake_placement, logic_controller.RIGHT_DIRECTION)

    def test_gets_left_direction(self) -> None:
        self.snake_placement[0] = np.array(['v', 'v', 'v', 'v'])
        self.snake_placement[1] = np.array(['v', 'h1', 'b2', 'v'])
        self.snake_placement[2] = np.array(['v', 'v', 'v', 'v'])
        self.snake_placement[3] = np.array(['v', 'v', 'v', 'v'])
        snake_placement = logic_controller.get_direction(self.snake_placement)
        self.assertEqual(snake_placement, logic_controller.LEFT_DIRECTION)

    def test_gets_top_direction(self) -> None:
        self.snake_placement[0] = np.array(['v', 'v', 'v', 'v'])
        self.snake_placement[1] = np.array(['v', 'h1', 'v', 'v'])
        self.snake_placement[2] = np.array(['v', 'b2', 'v', 'v'])
        self.snake_placement[3] = np.array(['v', 'v', 'v', 'v'])
        snake_placement = logic_controller.get_direction(self.snake_placement)
        self.assertEqual(snake_placement, logic_controller.TOP_DIRECTION)

    def test_gets_bottom_direction(self) -> None:
        self.snake_placement[0] = np.array(['v', 'v', 'v', 'v'])
        self.snake_placement[1] = np.array(['v', 'b2', 'v', 'v'])
        self.snake_placement[2] = np.array(['v', 'h1', 'v', 'v'])
        self.snake_placement[3] = np.array(['v', 'v', 'v', 'v'])
        snake_placement = logic_controller.get_direction(self.snake_placement)
        self.assertEqual(snake_placement, logic_controller.BOTTOM_DIRECTION)

    def test_raises_value_error_if_no_head_found(self) -> None:
        self.snake_placement[0] = np.array(['v', 'v', 'v', 'v'])
        self.snake_placement[1] = np.array(['v', 'b2', 'v', 'v'])
        self.snake_placement[2] = np.array(['v', 'b1', 'v', 'v'])
        self.snake_placement[3] = np.array(['v', 'v', 'v', 'v'])
        with self.assertRaises(ValueError):
            logic_controller.get_direction(self.snake_placement)

    def test_gets_right_direction_from_corner(self) -> None:
        self.snake_placement[0] = np.array(['v', 'b2', 'h1', 'v'])
        self.snake_placement[1] = np.array(['v', 'v', 'v', 'v'])
        self.snake_placement[2] = np.array(['v', 'v', 'v', 'v'])
        self.snake_placement[3] = np.array(['v', 'v', 'v', 'v'])
        snake_placement = logic_controller.get_direction(self.snake_placement)
        self.assertEqual(snake_placement, logic_controller.RIGHT_DIRECTION)

    def test_gets_left_direction_from_bottom_left_corner(self) -> None:
        # This is done to check the distinction on x and y bound
        self.snake_placement = np.empty((5, 2), dtype=np.object_)
        self.snake_placement[0] = np.array(['v', 'v'])
        self.snake_placement[1] = np.array(['v', 'v'])
        self.snake_placement[2] = np.array(['v', 'v'])
        self.snake_placement[3] = np.array(['v', 'v'])
        self.snake_placement[4] = np.array(['h1', 'b2'])
        snake_placement = logic_controller.get_direction(self.snake_placement)
        self.assertEqual(snake_placement, logic_controller.LEFT_DIRECTION)

    def test_gets_left_direction_from_bottom_right_corner(self) -> None:
        # This is done to check the distinction on x and y bound
        self.snake_placement = np.empty((5, 2), dtype=np.object_)
        self.snake_placement[0] = np.array(['v', 'v'])
        self.snake_placement[1] = np.array(['v', 'v'])
        self.snake_placement[2] = np.array(['v', 'v'])
        self.snake_placement[3] = np.array(['v', 'v'])
        self.snake_placement[4] = np.array(['b2', 'h1'])
        snake_placement = logic_controller.get_direction(self.snake_placement)
        self.assertEqual(snake_placement, logic_controller.RIGHT_DIRECTION)

    def test_gets_left_direction_from_top_right_corner(self) -> None:
        # This is done to check the distinction on x and y bound
        self.snake_placement = np.empty((5, 2), dtype=np.object_)
        self.snake_placement[0] = np.array(['b2', 'h1'])
        self.snake_placement[1] = np.array(['v', 'v'])
        self.snake_placement[2] = np.array(['v', 'v'])
        self.snake_placement[3] = np.array(['v', 'v'])
        self.snake_placement[4] = np.array(['v', 'v'])
        snake_placement = logic_controller.get_direction(self.snake_placement)
        self.assertEqual(snake_placement, logic_controller.RIGHT_DIRECTION)

    def test_gets_left_direction_from_top_left_corner(self) -> None:
        # This is done to check the distinction on x and y bound
        self.snake_placement = np.empty((5, 2), dtype=np.object_)
        self.snake_placement[0] = np.array(['h1', 'b2'])
        self.snake_placement[1] = np.array(['v', 'v'])
        self.snake_placement[2] = np.array(['v', 'v'])
        self.snake_placement[3] = np.array(['v', 'v'])
        self.snake_placement[4] = np.array(['v', 'v'])
        snake_placement = logic_controller.get_direction(self.snake_placement)
        self.assertEqual(snake_placement, logic_controller.LEFT_DIRECTION)
