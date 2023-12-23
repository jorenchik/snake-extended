from unittest import TestCase
from snakext.facades import pygame_facade
from snakext.state import state
import pygame
from unittest.mock import MagicMock


class TestMovementDirection(TestCase):

    def setUp(self) -> None:
        self.pygame_facade_instance = MagicMock()
        self.get_keys = MagicMock()

    def test_one_pressed_no_previous_keys_pressed(self) -> None:
        control_direction = state.LEFT_DIRECTION
        self.get_keys.return_value = [pygame_facade.K_LEFT]
        test_movement_direction = pygame_facade.movement_direction(
            [], self.get_keys)
        self.assertEqual(test_movement_direction, control_direction)

    def test_multiple_keys_pressed_no_previous_keys_pressed(self) -> None:
        control_direction = state.LEFT_DIRECTION
        self.get_keys.return_value = [pygame_facade.K_LEFT, pygame_facade.K_UP]
        test_movement_direction = pygame_facade.movement_direction(
            [], self.get_keys)
        # Should return first direction since no previous keys are present
        self.assertEqual(test_movement_direction, control_direction)

    def test_one_key_pressed_with_previous_keys_pressed(self) -> None:
        control_direction = state.LEFT_DIRECTION
        previous_keys = [pygame_facade.K_RIGHT, pygame_facade.K_DOWN]
        self.get_keys.return_value = [pygame_facade.K_LEFT, pygame_facade.K_UP]
        test_movement_direction = pygame_facade.movement_direction(
            previous_keys, self.get_keys)
        self.assertEqual(test_movement_direction, control_direction)

    def test_several_keys_pressed_with_previous_keys_pressed_where_one_is_new(
            self) -> None:
        control_direction = state.RIGHT_DIRECTION
        previous_keys = [pygame_facade.K_LEFT]
        self.get_keys.return_value = [
            pygame_facade.K_LEFT, pygame_facade.K_RIGHT
        ]
        test_movement_direction = pygame_facade.movement_direction(
            previous_keys, self.get_keys)
        self.assertEqual(test_movement_direction, control_direction)

    def test_2_keys_pressed_with_2_previous_keys_same_keys_pressed(
            self) -> None:
        control_direction = state.LEFT_DIRECTION
        previous_keys = [pygame_facade.K_LEFT, pygame_facade.K_RIGHT]
        self.get_keys.return_value = [
            pygame_facade.K_LEFT, pygame_facade.K_RIGHT
        ]
        test_movement_direction = pygame_facade.movement_direction(
            previous_keys, self.get_keys)
        self.assertEqual(test_movement_direction, control_direction)


class TestGetMovementKeys(TestCase):

    def setUp(self) -> None:
        self.pygame_module_mock = MagicMock()
        pygame_facade.init_game(self.pygame_module_mock)

    def test_gets_one_movement_input(self) -> None:
        control_keys = [pygame_facade.K_RIGHT]
        key_not_in_movement_list = 5
        return_events = [MagicMock(), MagicMock()]
        return_events[0].key = control_keys[0]
        return_events[1].key = key_not_in_movement_list
        return_events[0].type = pygame.KEYDOWN
        return_events[1].type = pygame.KEYDOWN
        self.pygame_module_mock.event.get.return_value = return_events
        test_keys = pygame_facade.movement_keys()
        self.assertEqual(test_keys, control_keys)

    def test_gets_two_movement_input(self) -> None:
        control_keys = [pygame_facade.K_RIGHT, pygame_facade.K_UP]
        key_not_in_movement_list = 5
        return_events = [MagicMock(), MagicMock(), MagicMock()]
        return_events[0].key = control_keys[0]
        return_events[1].key = control_keys[1]
        return_events[2].key = key_not_in_movement_list
        return_events[0].type = pygame.KEYDOWN
        return_events[1].type = pygame.KEYDOWN
        return_events[2].type = pygame.KEYDOWN
        self.pygame_module_mock.event.get.return_value = return_events
        test_keys = pygame_facade.movement_keys()
        self.assertEqual(test_keys, control_keys)

    def test_gets_zero_movement_input(self) -> None:
        control_keys = []
        key_not_in_movement_list = 5
        return_events = [MagicMock()]
        return_events[0].key = key_not_in_movement_list
        return_events[0].type = pygame.KEYDOWN
        self.pygame_module_mock.event.get.return_value = return_events
        test_keys = pygame_facade.movement_keys()
        self.assertEqual(test_keys, control_keys)
