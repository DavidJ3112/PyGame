from typing import List, Tuple
import pygame_gui
import threading
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

        self.ASPECTS_SCREEN = (640, 640)
        self.screen = pygame.display.set_mode(self.ASPECTS_SCREEN)
        self.BGC = (200, 200, 200)

        self.Clock = pygame.time.Clock()
        self.fps = 24
        self.drop_speed = 1000
        self.move_delay = self.drop_speed
        self.move_timer = 0

        self.new_piece = True
        self.board_size = (10, 20)
        self.board = self.ConstructBoard()

    def ConstructBoard(self):
        game_board_sizes = self.board_size
        self.board = []
        for _ in range(game_board_sizes[1]):
            current_row = []
            for _ in range(game_board_sizes[0]):
                current_row.append("")
            self.board.append(current_row)
        return self.board

    def Loop(self):
        ui = UI(self.screen)
        self.CreatePiece()
        while self.running:
            dt = self.Clock.tick(self.fps)
            self.screen.fill(self.BGC)
            self.CheckEvents()

            ui.DrawBoard(self.board, self.screen)

            pygame.display.flip()

            self.move_timer += dt

            if self.move_timer >= self.move_delay:
                self.Gravity()
                self.move_timer = 0

        pygame.quit()

    def LockPiece(self, active_blocks):
        for row, col, piece_name in active_blocks:
            self.board[row][col] = (piece_name, False)
        self.CreatePiece()

    def GetActives(self) -> List[Tuple[int, int, str]]:
        """
        Gets all active pices

        returns:
            [(row, col, piece_name)]
        """
        active_blocks = []

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] != "":
                    piece_name, active = self.board[row][col]

                    if active:
                        active_blocks.append((row, col, piece_name))
        
        return active_blocks

    def Gravity(self):
        active_blocks = self.GetActives()

        for row, col, _ in active_blocks:
            if row + 1 >= len(self.board):
                self.LockPiece(active_blocks)
                return

            below = self.board[row + 1][col]

            if below != "" and below[1] is False:
                self.LockPiece(active_blocks)
                return

        for row, col, piece_name in sorted(active_blocks, reverse=True):
            self.board[row][col] = ""
            self.board[row + 1][col] = (piece_name, True)

    def Movement(self, dir):
        active_blocks = self.GetActives()

        for row, col, _ in active_blocks:
            new_col = col + dir

            if new_col < 0 or new_col >= len(self.board[row]):
                return

            target = self.board[row][new_col]
            if target != "" and target[1] is False:
                return

            if dir == 1:
                active_blocks.sort(reverse=True)
            else:
                active_blocks.sort()

        for row, col, piece_name in active_blocks:
            self.board[row][col] = ""
            self.board[row][col + dir] = (piece_name, True)
    
    def Rotate(self):
        active_blocks = self.GetActives()

        if not active_blocks:
            return

        pivot_r, pivot_c, _ = active_blocks[0]

        new_positions = []

        # compute rotated positions first
        for row, col, piece_name in active_blocks:
            r0 = row - pivot_r
            c0 = col - pivot_c

            r1 = c0
            c1 = -r0

            new_r = r1 + pivot_r
            new_c = c1 + pivot_c

            # bounds check
            if new_r < 0 or new_r >= len(self.board):
                return
            if new_c < 0 or new_c >= len(self.board[0]):
                return

            # collision check
            target = self.board[new_r][new_c]
            if target != "" and target[1] is False:
                return

            new_positions.append((new_r, new_c, piece_name))

        # clear old piece
        for row, col, _ in active_blocks:
            self.board[row][col] = ""

        # place new piece correctly
        for r, c, name in new_positions:
            self.board[r][c] = (name, True)
            


    def CreatePiece(self):
        if self.new_piece:
            pieces = {
                "I": [(0, 1), (1, 1), (2, 1), (3, 1)],
                "O": [(1, 0), (0, 0), (1, 1), (0, 1)],
                "T": [(1, 0), (0, 1), (1, 1), (2, 1)],
                "S": [(1, 0), (2, 0), (0, 1), (1, 1)],
                "Z": [(0, 0), (1, 0), (1, 1), (2, 1)],
                "J": [(2, 0), (0, 1), (1, 1), (2, 1)],
                "L": [(0, 0), (0, 1), (1, 1), (2, 1)],
            }

            piece_name = random.choice(list(pieces.keys()))
            piece_shape = pieces[piece_name]

            print(piece_name, piece_shape)

            x_center = self.board_size[0] // 2 - 1

            for row, col in piece_shape:
                col += x_center
                self.board[row][col] = (piece_name, True)

    def CheckEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.move_delay = 10
            
                if event.key == pygame.K_LEFT:
                    self.Movement(-1)

                if event.key == pygame.K_RIGHT:
                    self.Movement(1)

                if event.key == pygame.K_UP:
                    self.Rotate()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.move_delay = self.drop_speed


if __name__ == "__main__":
    game = Game()
    game.Loop()
