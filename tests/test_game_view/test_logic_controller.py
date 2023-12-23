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
        self.snake_placement = np.empty((4, 4), dtype=np.object_)
        self.head = state.SNAKE_HEAD_PLACE
        self.body = state.SNAKE_BODY_PLACE
        self.tail = state.SNAKE_TAIL_PLACE
        self.snake_placement[0] = ['v', 'v', 'v', 'v']
        self.snake_placement[1] = [
            f"{self.tail}2", f"{self.body}1", f"{self.head}0", 'v'
        ]
        self.snake_placement[2] = ['v', 'v', 'v', 'v']
        self.snake_placement[3] = ['v', 'v', 'v', 'v']

    def test_moves_right_space_available(self) -> None:
        self.snake_placement = logic_controller.move_snake(
            self.snake_placement, state.RIGHT_DIRECTION,
            state.RIGHT_DIRECTION)[0]
        new_snake_placement = np.empty((4, 4), dtype=np.object_)
        new_snake_placement[0] = ['v', 'v', 'v', 'v']
        new_snake_placement[1] = [
            'v', f"{self.tail}2", f"{self.body}1", f"{self.head}0"
        ]
        new_snake_placement[2] = ['v', 'v', 'v', 'v']
        new_snake_placement[3] = ['v', 'v', 'v', 'v']
        self.assertTrue(
            np.array_equal(self.snake_placement, new_snake_placement),
            f"{new_snake_placement} is different from {self.snake_placement}")

    def test_moves_right_and_add_to_snake(self) -> None:
        self.snake_placement = logic_controller.move_snake(
            self.snake_placement,
            state.RIGHT_DIRECTION,
            state.RIGHT_DIRECTION,
            add_to_snake=True)[0]
        new_snake_placement = np.empty((4, 4), dtype=np.object_)
        new_snake_placement[0] = ['v', 'v', 'v', 'v']
        new_snake_placement[1] = [
            f"{self.tail}3", f"{self.body}2", f"{self.body}1", f"{self.head}0"
        ]
        new_snake_placement[2] = ['v', 'v', 'v', 'v']
        new_snake_placement[3] = ['v', 'v', 'v', 'v']
        self.assertTrue(
            np.array_equal(self.snake_placement, new_snake_placement),
            f"{self.snake_placement} is different from expected {new_snake_placement}"
        )

    def test_moves_down_space_available(self) -> None:
        self.snake_placement = logic_controller.move_snake(
            self.snake_placement, state.RIGHT_DIRECTION,
            state.BOTTOM_DIRECTION)[0]
        new_snake_placement = np.empty((4, 4), dtype=np.object_)
        new_snake_placement[0] = ['v', 'v', 'v', 'v']
        new_snake_placement[1] = ['v', f"{self.tail}2", f"{self.body}1", 'v']
        new_snake_placement[2] = ['v', 'v', f"{self.head}0", 'v']
        new_snake_placement[3] = ['v', 'v', 'v', 'v']
        self.assertTrue(
            np.array_equal(self.snake_placement, new_snake_placement),
            f"{new_snake_placement} is different from {self.snake_placement}")

    def test_moves_up_space_available(self) -> None:
        self.snake_placement = logic_controller.move_snake(
            self.snake_placement, state.RIGHT_DIRECTION,
            state.TOP_DIRECTION)[0]
        new_snake_placement = np.empty((4, 4), dtype=np.object_)
        new_snake_placement[0] = ['v', 'v', f"{self.head}0", 'v']
        new_snake_placement[1] = ['v', f"{self.tail}2", f"{self.body}1", 'v']
        new_snake_placement[2] = ['v', 'v', 'v', 'v']
        new_snake_placement[3] = ['v', 'v', 'v', 'v']
        self.assertTrue(
            np.array_equal(self.snake_placement, new_snake_placement),
            f"{new_snake_placement} is different from {self.snake_placement}")

    def test_moves_left_space_available(self) -> None:
        snake_placement = np.empty((4, 4), dtype=np.object_)
        snake_placement[0] = ['v', 'v', 'v', 'v']
        snake_placement[1] = [
            'v', f"{self.head}0", f"{self.body}1", f"{self.tail}2"
        ]
        snake_placement[2] = ['v', 'v', 'v', 'v']
        snake_placement[3] = ['v', 'v', 'v', 'v']
        self.snake_placement = snake_placement
        self.snake_placement = logic_controller.move_snake(
            self.snake_placement, state.LEFT_DIRECTION,
            state.LEFT_DIRECTION)[0]
        new_snake_placement = np.empty((4, 4), dtype=np.object_)
        new_snake_placement[0] = ['v', 'v', 'v', 'v']
        new_snake_placement[1] = [
            f"{self.head}0", f"{self.body}1", f"{self.tail}2", 'v'
        ]
        new_snake_placement[2] = ['v', 'v', 'v', 'v']
        new_snake_placement[3] = ['v', 'v', 'v', 'v']
        self.assertTrue(
            np.array_equal(self.snake_placement, new_snake_placement),
            f"{new_snake_placement} is different from {self.snake_placement}")

    def test_moves_right_opposite_direction(self) -> None:
        snake_placement = np.empty((4, 4), dtype=np.object_)
        snake_placement[0] = ['v', 'v', 'v', 'v']
        snake_placement[1] = [
            'v', f"{self.head}0", f"{self.body}1", f"{self.tail}2"
        ]
        snake_placement[2] = ['v', 'v', 'v', 'v']
        snake_placement[3] = ['v', 'v', 'v', 'v']
        self.snake_placement = snake_placement
        self.snake_placement = logic_controller.move_snake(
            self.snake_placement, state.LEFT_DIRECTION,
            state.RIGHT_DIRECTION)[0]
        new_snake_placement = np.empty((4, 4), dtype=np.object_)
        new_snake_placement[0] = ['v', 'v', 'v', 'v']
        new_snake_placement[1] = [
            f"{self.head}0", f"{self.body}1", f"{self.tail}2", 'v'
        ]
        new_snake_placement[2] = ['v', 'v', 'v', 'v']
        new_snake_placement[3] = ['v', 'v', 'v', 'v']
        self.assertTrue(
            np.array_equal(self.snake_placement, new_snake_placement),
            f"{new_snake_placement} is different from {self.snake_placement}")

    def test_moves_bottom_opposite_direction(self) -> None:
        snake_placement = np.empty((4, 4), dtype=np.object_)
        snake_placement[0] = ['v', 'v', 'v', 'v']
        snake_placement[1] = ['v', 'v', f"{self.head}0", 'v']
        snake_placement[2] = ['v', 'v', f"{self.body}1", 'v']
        snake_placement[3] = ['v', 'v', f"{self.tail}2", 'v']
        self.snake_placement = snake_placement
        new_snake_placement = np.empty((4, 4), dtype=np.object_)
        new_snake_placement[0] = ['v', 'v', f"{self.head}0", 'v']
        new_snake_placement[1] = ['v', 'v', f"{self.body}1", 'v']
        new_snake_placement[2] = ['v', 'v', f"{self.tail}2", 'v']
        new_snake_placement[3] = ['v', 'v', 'v', 'v']
        self.snake_placement = logic_controller.move_snake(
            self.snake_placement, state.TOP_DIRECTION,
            state.BOTTOM_DIRECTION)[0]
        self.assertTrue(
            np.array_equal(self.snake_placement, new_snake_placement),
            f"{self.snake_placement} is different from {new_snake_placement}")

    def test_moves_top_opposite_direction(self) -> None:
        snake_placement = np.empty((4, 4), dtype=np.object_)
        snake_placement[0] = ['v', 'v', f"{self.tail}2", 'v']
        snake_placement[1] = ['v', 'v', f"{self.body}1", 'v']
        snake_placement[2] = ['v', 'v', f"{self.head}0", 'v']
        snake_placement[3] = ['v', 'v', 'v', 'v']
        self.snake_placement = snake_placement
        new_snake_placement = np.empty((4, 4), dtype=np.object_)
        new_snake_placement[0] = ['v', 'v', 'v', 'v']
        new_snake_placement[1] = ['v', 'v', f"{self.tail}2", 'v']
        new_snake_placement[2] = ['v', 'v', f"{self.body}1", 'v']
        new_snake_placement[3] = ['v', 'v', f"{self.head}0", 'v']
        self.snake_placement = logic_controller.move_snake(
            self.snake_placement, state.BOTTOM_DIRECTION,
            state.TOP_DIRECTION)[0]
        self.assertTrue(
            np.array_equal(self.snake_placement, new_snake_placement),
            f"{self.snake_placement} is different from {new_snake_placement}")

    def test_moves_left_opposite_direction(self) -> None:
        snake_placement = np.empty((4, 4), dtype=np.object_)
        snake_placement[0] = ['v', 'v', 'v', 'v']
        snake_placement[1] = [
            f"{self.tail}2",
            f"{self.body}1",
            f"{self.head}0",
            'v',
        ]
        snake_placement[2] = ['v', 'v', 'v', 'v']
        snake_placement[3] = ['v', 'v', 'v', 'v']
        self.snake_placement = snake_placement
        self.snake_placement = logic_controller.move_snake(
            self.snake_placement, state.RIGHT_DIRECTION,
            state.LEFT_DIRECTION)[0]
        new_snake_placement = np.empty((4, 4), dtype=np.object_)
        new_snake_placement[0] = ['v', 'v', 'v', 'v']
        new_snake_placement[1] = [
            'v',
            f"{self.tail}2",
            f"{self.body}1",
            f"{self.head}0",
        ]
        new_snake_placement[2] = ['v', 'v', 'v', 'v']
        new_snake_placement[3] = ['v', 'v', 'v', 'v']
        self.assertTrue(
            np.array_equal(self.snake_placement, new_snake_placement),
            f"{self.snake_placement} is different from {new_snake_placement}")

    def test_moves_the_same_no_movement_key(self) -> None:
        snake_placement = np.empty((4, 4), dtype=np.object_)
        snake_placement[0] = ['v', 'v', 'v', 'v']
        snake_placement[1] = [
            'v', f"{self.head}0", f"{self.body}1", f"{self.tail}2"
        ]
        snake_placement[2] = ['v', 'v', 'v', 'v']
        snake_placement[3] = ['v', 'v', 'v', 'v']
        self.snake_placement = snake_placement
        self.snake_placement = logic_controller.move_snake(
            self.snake_placement, state.LEFT_DIRECTION, 0)[0]
        new_snake_placement = np.empty((4, 4), dtype=np.object_)
        new_snake_placement[0] = ['v', 'v', 'v', 'v']
        new_snake_placement[1] = [
            f"{self.head}0", f"{self.body}1", f"{self.tail}2", 'v'
        ]
        new_snake_placement[2] = ['v', 'v', 'v', 'v']
        new_snake_placement[3] = ['v', 'v', 'v', 'v']
        self.assertTrue(
            np.array_equal(self.snake_placement, new_snake_placement),
            f"{new_snake_placement} is different from {self.snake_placement}")

    def test_moves_right_and_jumps_to_other_side_space_available(self) -> None:
        snake_placement = np.empty((4, 4), dtype=np.object_)
        snake_placement[0] = ['v', 'v', 'v', 'v']
        snake_placement[1] = [
            'v', f"{self.tail}2", f"{self.body}1", f"{self.head}0"
        ]
        snake_placement[2] = ['v', 'v', 'v', 'v']
        snake_placement[3] = ['v', 'v', 'v', 'v']
        new_snake_placement = np.empty((4, 4), dtype=np.object_)
        new_snake_placement[0] = ['v', 'v', 'v', 'v']
        new_snake_placement[1] = [
            f"{self.head}0",
            'v',
            f"{self.tail}2",
            f"{self.body}1",
        ]
        new_snake_placement[2] = ['v', 'v', 'v', 'v']
        new_snake_placement[3] = ['v', 'v', 'v', 'v']
        self.snake_placement = snake_placement
        self.snake_placement = logic_controller.move_snake(
            self.snake_placement, state.RIGHT_DIRECTION,
            state.RIGHT_DIRECTION)[0]
        self.assertTrue(
            np.array_equal(self.snake_placement, new_snake_placement),
            f"{new_snake_placement} is different from {self.snake_placement}")

    def test_moves_down_and_jumps_to_other_side_space_available(self) -> None:
        self.snake_placement = logic_controller.move_snake(
            self.snake_placement, state.RIGHT_DIRECTION,
            state.BOTTOM_DIRECTION)[0]
        snake_placement = np.empty((4, 4), dtype=np.object_)
        snake_placement[0] = ['v', 'v', 'v', 'v']
        snake_placement[1] = ['v', 'v', f"{self.tail}2", 'v']
        snake_placement[2] = ['v', 'v', f"{self.body}1", 'v']
        snake_placement[3] = ['v', 'v', f"{self.head}1", 'v']
        self.snake_placement = snake_placement

        new_snake_placement = np.empty((4, 4), dtype=np.object_)
        new_snake_placement[0] = ['v', 'v', f"{self.head}0", 'v']
        new_snake_placement[1] = ['v', 'v', 'v', 'v']
        new_snake_placement[2] = ['v', 'v', f"{self.tail}2", 'v']
        new_snake_placement[3] = ['v', 'v', f"{self.body}1", 'v']

        self.snake_placement = logic_controller.move_snake(
            self.snake_placement, state.BOTTOM_DIRECTION,
            state.BOTTOM_DIRECTION)[0]

        self.assertTrue(
            np.array_equal(self.snake_placement, new_snake_placement),
            f"{new_snake_placement} is different from {self.snake_placement}")

    def test_moves_up_and_jumps_to_other_side_space_available(self) -> None:
        # TODO: rework
        self.snake_placement = logic_controller.move_snake(
            self.snake_placement, state.RIGHT_DIRECTION,
            state.TOP_DIRECTION)[0]
        new_snake_placement = np.empty((4, 4), dtype=np.object_)
        new_snake_placement[0] = ['v', 'v', f"{self.head}0", 'v']
        new_snake_placement[1] = ['v', f"{self.tail}2", f"{self.body}1", 'v']
        new_snake_placement[2] = ['v', 'v', 'v', 'v']
        new_snake_placement[3] = ['v', 'v', 'v', 'v']

        self.assertTrue(
            np.array_equal(self.snake_placement, new_snake_placement),
            f"{new_snake_placement} is different from {self.snake_placement}")

    def test_moves_left_and_jumps_to_other_side_space_available(self) -> None:
        # TODO: rework
        snake_placement = np.empty((4, 4), dtype=np.object_)
        snake_placement[0] = ['v', 'v', 'v', 'v']
        snake_placement[1] = [
            'v', f"{self.head}0", f"{self.body}1", f"{self.tail}2"
        ]
        snake_placement[2] = ['v', 'v', 'v', 'v']
        snake_placement[3] = ['v', 'v', 'v', 'v']
        self.snake_placement = snake_placement
        self.snake_placement = logic_controller.move_snake(
            self.snake_placement, state.LEFT_DIRECTION,
            state.LEFT_DIRECTION)[0]
        new_snake_placement = np.empty((4, 4), dtype=np.object_)
        new_snake_placement[0] = ['v', 'v', 'v', 'v']
        new_snake_placement[1] = [
            f"{self.head}0", f"{self.body}1", f"{self.tail}2", 'v'
        ]
        new_snake_placement[2] = ['v', 'v', 'v', 'v']
        new_snake_placement[3] = ['v', 'v', 'v', 'v']
        self.assertTrue(
            np.array_equal(self.snake_placement, new_snake_placement),
            f"{new_snake_placement} is different from {self.snake_placement}")


class TestCheckCollision(TestCase):

    def setUp(self) -> None:
        self.placement1 = np.empty((4, 4), dtype=np.object_)
        self.placement2 = np.empty((4, 4), dtype=np.object_)
        self.head = state.SNAKE_HEAD_PLACE
        self.body = state.SNAKE_BODY_PLACE
        self.tail = state.SNAKE_TAIL_PLACE

    def test_find_collision(self):
        placement1 = np.empty((4, 4), dtype=np.object_)
        placement1[0] = ['v', 'v', 'v', 'v']
        placement1[1] = [
            f"{self.tail}2", f"{self.body}1", f"{self.head}0", 'v'
        ]
        placement1[2] = ['v', 'v', 'v', 'v']
        placement1[3] = ['v', 'v', 'v', 'v']
        self.placement1 = placement1

        placement2 = np.empty((4, 4), dtype=np.object_)
        placement2[0] = ['v', 'v', 'v', 'v']
        placement2[1] = ['v', 'v', f"{self.tail}2", 'v']
        placement2[2] = ['v', 'v', f"{self.body}1", 'v']
        placement2[3] = ['v', 'v', f"{self.head}0", 'v']
        self.placement2 = placement2

        collision_coordinates = logic_controller._search_collision(
            self.placement1, self.placement2)
        self.assertEqual((1, 2), collision_coordinates)

    def test_find_collision_collides_only_body(self):
        placement1 = np.empty((4, 4), dtype=np.object_)
        placement1[0] = ['v', 'v', 'v', 'v']
        placement1[1] = [
            f"{self.tail}3",
            f"{self.body}2",
            f"{self.body}1",
            f"{self.head}0",
        ]
        placement1[2] = ['v', 'v', 'v', 'v']
        placement1[3] = ['v', 'v', 'v', 'v']
        self.placement1 = placement1

        placement2 = np.empty((4, 4), dtype=np.object_)
        placement2[0] = ['v', 'v', 'v', 'v']
        placement2[1] = ['v', 'v', f"{self.tail}2", 'v']
        placement2[2] = ['v', 'v', f"{self.body}1", 'v']
        placement2[3] = ['v', 'v', f"{self.head}0", 'v']
        self.placement2 = placement2

        collision_coordinates = logic_controller._search_collision(
            self.placement1, self.placement2)
        self.assertEqual((1, 2), collision_coordinates)

    def test_find_collision_only_head_finds(self):
        placement1 = np.empty((4, 4), dtype=np.object_)
        placement1[0] = ['v', 'v', 'v', 'v']
        placement1[1] = [
            f"{self.tail}2", f"{self.body}1", f"{self.head}0", 'v'
        ]
        placement1[2] = ['v', 'v', 'v', 'v']
        placement1[3] = ['v', 'v', 'v', 'v']
        self.placement1 = placement1

        placement2 = np.empty((4, 4), dtype=np.object_)
        placement2[0] = ['v', 'v', 'v', 'v']
        placement2[1] = ['v', 'v', f"{self.tail}2", 'v']
        placement2[2] = ['v', 'v', f"{self.body}1", 'v']
        placement2[3] = ['v', 'v', f"{self.head}0", 'v']
        self.placement2 = placement2

        collision_coordinates = logic_controller._search_collision(
            self.placement1, self.placement2, only_head=True)
        self.assertEqual((1, 2), collision_coordinates)

    def test_find_collision_only_head_collides_only_body(self):
        placement1 = np.empty((4, 4), dtype=np.object_)
        placement1[0] = ['v', 'v', 'v', 'v']
        placement1[1] = [
            f"{self.tail}3", f"{self.body}2", f"{self.body}1", f"{self.head}0"
        ]
        placement1[2] = ['v', 'v', 'v', 'v']
        placement1[3] = ['v', 'v', 'v', 'v']
        self.placement1 = placement1

        placement2 = np.empty((4, 4), dtype=np.object_)
        placement2[0] = ['v', 'v', 'v', 'v']
        placement2[1] = ['v', 'v', f"{self.tail}2", 'v']
        placement2[2] = ['v', 'v', f"{self.body}1", 'v']
        placement2[3] = ['v', 'v', f"{self.head}0", 'v']
        self.placement2 = placement2

        collision_coordinates = logic_controller._search_collision(
            self.placement1, self.placement2, only_head=True)
        self.assertEqual(logic_controller.COORDINATES_NOT_FOUND,
                         collision_coordinates)

    def test_collistion_not_found(self):
        placement1 = np.empty((4, 4), dtype=np.object_)
        placement1[0] = ['v', 'v', 'v', 'v']
        placement1[1] = [f"{self.tail}2", f"{self.body}1", 'v', 'v']
        placement1[2] = ['v', f"{self.head}0", 'v', 'v']
        placement1[3] = ['v', 'v', 'v', 'v']
        self.placement1 = placement1

        placement2 = np.empty((4, 4), dtype=np.object_)
        placement2[0] = ['v', 'v', 'v', 'v']
        placement2[1] = ['v', 'v', f"{self.tail}2", 'v']
        placement2[2] = ['v', 'v', f"{self.body}1", 'v']
        placement2[3] = ['v', 'v', f"{self.head}0", 'v']
        self.placement2 = placement2

        collision_coordinates = logic_controller._search_collision(
            self.placement1, self.placement2)
        self.assertEqual(logic_controller.COORDINATES_NOT_FOUND,
                         collision_coordinates)


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
        post_snake_placement[position[0],
                             position[1]] = logic_controller.INITIAL_BODY_PLACE
        post_snake_placement[position[0],
                             position[1] + 1] = logic_controller.HEAD_PLACE
        post_snake_placement[position[0], position[1] -
                             1] = logic_controller.INITIAL_TAIL_PLACE
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


class TestPlaceInitialSnake(TestCase):

    def setUp(self) -> None:
        self.food_placement = np.full((4, 4), 'v', dtype=np.object_)
        self.other_placement = np.full((4, 4), 'v', dtype=np.object_)
        self.head = state.SNAKE_HEAD_PLACE
        self.body = state.SNAKE_BODY_PLACE
        self.tail = state.SNAKE_TAIL_PLACE

    def test_places_food_with_available_places(self) -> None:
        choose_function = MagicMock()
        position = 0, 1
        choose_function.return_value = position

        placement1 = np.empty((4, 4), dtype=np.object_)
        placement1[0] = ['v', 'v', 'v', 'v']
        placement1[1] = [f"{self.tail}2", f"{self.body}1", 'v', 'v']
        placement1[2] = ['v', f"{self.head}0", 'v', 'v']
        placement1[3] = ['v', 'v', 'v', 'v']
        self.other_placement = placement1

        placement2 = np.empty((4, 4), dtype=np.object_)
        placement2[0] = ['v', 'v', 'v', 'f']
        placement2[1] = ['v', 'f', 'v', 'v']
        placement2[2] = ['v', 'v', 'v', 'f']
        placement2[3] = ['v', 'v', 'v', 'v']
        self.food_placement = placement2

        placement3 = np.empty((4, 4), dtype=np.object_)
        placement3[0] = ['v', 'f', 'v', 'f']
        placement3[1] = ['v', 'f', 'v', 'v']
        placement3[2] = ['v', 'v', 'v', 'f']
        placement3[3] = ['v', 'v', 'v', 'v']
        self.food_placement = placement2
        self.snake_placement = logic_controller.place_food(
            self.food_placement, self.other_placement, choose_function,
            state.FOOD_PLACE)
        self.assertTrue(
            np.array_equal(self.snake_placement, placement3),
            f"{self.snake_placement} is different from {placement3}")
