import unittest
from unittest.mock import Mock, MagicMock
from unittest import mock
import numpy
import numpy.typing as npt
from snakext.facades import pygame_facade
from snakext.views import game_view, playground
import pygame

SNAKE_BODY = 'b'
SNAKE_HEAD = 'h'
SNAKE_TAIL = 't'


class TestPlaceSnake(unittest.TestCase):
    b = SNAKE_BODY
    h = SNAKE_HEAD
    t = SNAKE_TAIL
    playground_instance: Mock
    pygame_facade: Mock

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        pygame_facade.init_game()

    def setUp(self) -> None:
        super().setUp()
        self.playground_instance = Mock()
        self.pygame_facade = Mock()
        self.pygame_facade.Rect = pygame.Rect
        self.snake_placement = numpy.empty((4, 4), dtype=numpy.str_)
        for i in range(0, 4):
            self.snake_placement[i] = numpy.array(['v' for x in range(0, 4)])
        self.grid: npt.NDArray[Mock] = numpy.empty((4, 4), dtype=Mock)
        for i in range(0, 4):
            for j in range(0, 4):
                self.grid[i, j] = MagicMock(spec=pygame_facade.Rect)

    def test_draws_tail_at_the_edge(self) -> None:
        self.snake_placement[1] = numpy.array(['v', self.t, self.b, self.h])
        game_view._place_snake(self.pygame_facade, self.playground_instance,
                               self.snake_placement, self.grid)
        self.pygame_facade.draw_rect.assert_any_call(self.grid[1, 1],
                                                     game_view.SNAKE_COLOR)
        self.pygame_facade.draw_rect.assert_any_call(self.grid[1, 2],
                                                     game_view.SNAKE_COLOR)
        self.pygame_facade.draw_rect.assert_any_call(self.grid[1, 3],
                                                     game_view.SNAKE_COLOR)

    def test_draws_at_corner(self) -> None:
        self.snake_placement[0] = numpy.array(['v', 'v', 'v', self.h])
        self.snake_placement[1] = numpy.array(['v', 'v', 'v', 'v'])
        game_view._place_snake(self.pygame_facade, self.playground_instance,
                               self.snake_placement, self.grid)
        self.pygame_facade.draw_rect.assert_any_call(self.grid[0, 3],
                                                     game_view.SNAKE_COLOR)

    def test_draws_exact_amount(self) -> None:
        self.snake_placement[0] = numpy.array(['v', 'v', 'v', self.h])
        self.snake_placement[1] = numpy.array([self.b, 'v', 'v', self.h])
        game_view._place_snake(self.pygame_facade, self.playground_instance,
                               self.snake_placement, self.grid)
        self.pygame_facade.draw_rect.assert_has_calls([
            mock.call(self.grid[0, 3], game_view.SNAKE_COLOR),
            mock.call(self.grid[1, 0], game_view.SNAKE_COLOR)
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

    @classmethod
    def tearDownClass(cls):
        pygame.quit()
        super().tearDownClass()
