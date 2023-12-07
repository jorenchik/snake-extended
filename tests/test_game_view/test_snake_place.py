import unittest
from unittest.mock import Mock, MagicMock
from unittest import mock
import numpy
import numpy.typing as npt
from snakext.facades import pygame_facade
from snakext.state import state
from snakext.views import game_view, playground
import pygame


class TestPlaceSnake(unittest.TestCase):
    playground_instance: Mock
    pygame_facade_instance: Mock
    grid: numpy.ndarray[tuple[int, int], numpy.dtype[numpy.object_]]
    snake_color: pygame_facade.Color

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        pygame_facade.init_game()

    def setUp(self) -> None:
        super().setUp()
        self.playground_instance = Mock()
        self.pygame_facade = Mock()
        self.pygame_facade.Rect = pygame.Rect
        self.snake_color = pygame_facade.Color(*playground.snake_color)
        self.playground_instance.snake_color = self.snake_color
        self.snake_placement = numpy.empty((4, 4), dtype=numpy.object_)
        for i in range(0, 4):
            self.snake_placement[i] = numpy.array(["v" for x in range(0, 4)])
        self.grid: npt.NDArray[Mock] = numpy.empty((4, 4), dtype=Mock)
        for i in range(0, 4):
            for j in range(0, 4):
                self.grid[i, j] = MagicMock(spec=pygame_facade.Rect)

    def test_draws_tail_at_the_edge(self) -> None:
        self.snake_placement[1] = numpy.array([
            'v', state.SNAKE_TAIL_PLACE + "3", state.SNAKE_BODY_PLACE + "2",
            state.SNAKE_HEAD_PLACE + "1"
        ])
        game_view._place_snake(self.pygame_facade, self.playground_instance,
                               self.snake_placement, self.grid)
        self.pygame_facade.draw_rect.assert_any_call(self.grid[1, 1],
                                                     self.snake_color)
        self.pygame_facade.draw_rect.assert_any_call(self.grid[1, 2],
                                                     self.snake_color)
        self.pygame_facade.draw_rect.assert_any_call(self.grid[1, 3],
                                                     self.snake_color)

    def test_draws_at_corner(self) -> None:
        self.snake_placement[0] = numpy.array(
            ['v', 'v', 'v', state.SNAKE_BODY_PLACE + "1"])
        self.snake_placement[1] = numpy.array(['v', 'v', 'v', 'v'])
        game_view._place_snake(self.pygame_facade, self.playground_instance,
                               self.snake_placement, self.grid)
        self.pygame_facade.draw_rect.assert_has_calls(
            [mock.call(self.grid[0, 3], self.snake_color)],
            f"Position [{0}, {3}] is not called")

    def test_draws_exact_amount(self) -> None:
        self.snake_placement[0] = numpy.array(
            ['v', 'v', 'v', state.SNAKE_HEAD_PLACE + "1"])
        self.snake_placement[1] = numpy.array(
            [state.SNAKE_BODY_PLACE, 'v', 'v', state.SNAKE_HEAD_PLACE])
        game_view._place_snake(self.pygame_facade, self.playground_instance,
                               self.snake_placement, self.grid)
        self.pygame_facade.draw_rect.assert_has_calls([
            mock.call(self.grid[0, 3], self.snake_color),
            mock.call(self.grid[1, 0], self.snake_color)
        ])

    def test_executes_with_no_bodyparts(self) -> None:
        game_view._place_snake(self.pygame_facade, self.playground_instance,
                               self.snake_placement, self.grid)
        self.pygame_facade.draw_rect.assert_has_calls([])

    def test_raises_exception_on_unexpected_grid(self) -> None:
        self.grid[1, 1] = MagicMock()
        self.assertRaises(TypeError, game_view._place_snake,
                          self.pygame_facade, self.playground_instance,
                          self.snake_placement, self.grid)

    def test_places_only_snake_related_strings_in_placement(self) -> None:
        self.snake_placement[1] = [
            'm', state.SNAKE_TAIL_PLACE + "3", state.SNAKE_BODY_PLACE + "2",
            state.SNAKE_TAIL_PLACE + "1"
        ]
        game_view._place_snake(self.pygame_facade, self.playground_instance,
                               self.snake_placement, self.grid)
        self.assertNotIn(
            mock.call(self.grid[1, 0], self.snake_color),
            self.pygame_facade.draw_rect.mock_calls,
            "place_snake should not place places that are not snake.")

    @classmethod
    def tearDownClass(cls) -> None:
        pygame.quit()
        super().tearDownClass()
