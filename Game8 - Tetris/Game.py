import pygame_gui
import pygame
import random
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from general_scripts.Helpers import console
from Scripts.Ui import UI



class Game:
    def __init__(self) -> None:
        self.running = True

        self.ASPECTS_SCREEN = (640,640)
        self.screen = pygame.display.set_mode(self.ASPECTS_SCREEN)
        self.BGC = (200, 200, 200)

        self.Clock = pygame.time.Clock()
        self.fps = 24

        self.board_size = (10, 20)
        self.board = self.construct_board()

    def construct_board(self):
        game_board_sizes = (self.board_size)
        self.board = []
        for _ in range(game_board_sizes[1]):
            current_row = []
            for _ in range(game_board_sizes[0]):
                current_row.append("")
            self.board.append(current_row)
        return self.board

    def Loop(self):
        ui = UI(self.screen)
        while self.running:
            self.screen.fill(self.BGC)
            self.Clock.tick(self.fps)
            self.Check_Events()

            ui.DrawBoard(self.board, self.screen)

            pygame.display.flip()
        
        pygame.quit

    def Check_Events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    



if __name__ == "__main__":
    game = Game()
    game.Loop()