import pygame_gui
import os, sys
import pygame
import json
import time
from typing import (
    Any,
    Optional,
    Union,
    Callable,
    Iterable,
    Generator,
    TypeVar,
    Protocol,
    Literal,
)

class GameLevel():
    def __init__(self, screen, level_index=0) -> None:
        self.level_index = level_index
        self.Clock = pygame.time.Clock()
        self.fps = 24
        self.BGC = (25, 25, 25)
        self.screen = screen
        self.Running = True

        pass

    def loop(self, level_index):
        self.level_index = level_index
        while self.Running:
            dt = self.Clock.tick(self.fps)
            self.screen.fill(self.BGC)
            pygame.display.flip

class GameMenu():
    def __init__(self) -> None:
        SCREEN_RATIO = (640, 640)
        self.screen = pygame.display.set_mode(SCREEN_RATIO)
        pygame.display.set_caption("PvZ But Sceer")

        self.level_index = 5

        self.RunLevel = GameLevel(self.screen)

    def loop(self):
        while True:
            self.RunLevel.loop(self.level_index)


if __name__ == "__main__":
    menu = GameMenu()
    menu.loop()