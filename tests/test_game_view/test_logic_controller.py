from unittest import TestCase
from snakext.logic import logic_controller
from snakext.facades import pygame_facade
from snakext.state import state
import numpy as np
import pygame
from unittest.mock import MagicMock


class TestMoveSnake(TestCase):

    def setUp(self) -> None:
        self.snake_placement = np.empty((4, 4), dtype=np.object_)
        for i in range(0, 4):
            self.snake_placement[i] = np.array(['v' for x in range(0, 4)])
