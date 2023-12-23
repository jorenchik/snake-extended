from unittest import TestCase
from snakext.logic import logic_controller
from snakext.facades import pygame_facade
from snakext.state import state
import numpy as np
import pygame
from unittest.mock import MagicMock

SNAKE_INITIAL_PLACE = f"{state.SNAKE_HEAD_PLACE}0"


class TestMoveSnake(TestCase):

    def setUp(self) -> None:
        self.snake_placement = np.full((4, 4), 'v', dtype=np.object_)


class TestPlaceInitialSnake(TestCase):

    def setUp(self) -> None:
        self.snake_placement = np.full((4, 4), 'v', dtype=np.object_)

    def test_places_snake_to_empty_field(self) -> None:
        choose_function = MagicMock()
        position = 1, 2
        choose_function.return_value = position
        post_snake_placement = np.copy(self.snake_placement)
        self.snake_placement = logic_controller.place_initial_snake(
            self.snake_placement, choose_function)
        post_snake_placement[position[0], position[1]] = SNAKE_INITIAL_PLACE
        self.assertTrue(
            np.array_equal(self.snake_placement, post_snake_placement),
            f"{post_snake_placement} is different from {self.snake_placement}")

    def test_raise_value_error_if_a_snake_is_already_present(self) -> None:
        choose_function = MagicMock()
        position = 1, 2
        choose_function.return_value = position
        self.snake_placement[2, 2] = SNAKE_INITIAL_PLACE
        self.assertRaises(ValueError, logic_controller.place_initial_snake,
                          self.snake_placement, choose_function)
