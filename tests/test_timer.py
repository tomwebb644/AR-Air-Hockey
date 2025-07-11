import os

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classes import Timer


def test_timer_decrements_seconds():
    pygame.init()
    try:
        timer = Timer(None, 20)
        initial_min = timer.min
        initial_seconds = timer.seconds
        timer.update(1000)
        assert timer.min == initial_min
        assert timer.seconds < initial_seconds
    finally:
        pygame.quit()
