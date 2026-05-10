from typing import List, Tuple, Union
import pygame
import random
import sys
import os
import datetime
import itertools
import time
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from general_scripts.ANSI import ANSI
from general_scripts.Helpers import console

try:
    from Scripts.Ui import UI
except ImportError:
    UI = None

CellType = Union[str, Tuple[str, bool]]


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.running = True

        self.debug = False
        self.paused = False
        self.god_mode = False

        self.ASPECTS_SCREEN = (640, 640)
        self.screen = pygame.display.set_mode(self.ASPECTS_SCREEN)
        self.BGC = (200, 200, 200)

        self.pieces = {
            "I": {"blocks": [(0, 1), (1, 1), (2, 1), (3, 1)], "pivot": [1.5, 1.5]},
            "O": {"blocks": [(0, 0), (1, 0), (0, 1), (1, 1)], "pivot": [0.5, 0.5]},
            "T": {"blocks": [(1, 0), (0, 1), (1, 1), (2, 1)], "pivot": [1, 1]},
            "L": {"blocks": [(0, 0), (0, 1), (1, 1), (2, 1)], "pivot": [1, 1]},
            "J": {"blocks": [(2, 0), (0, 1), (1, 1), (2, 1)], "pivot": [1, 1]},
            "S": {"blocks": [(1, 0), (2, 0), (0, 1), (1, 1)], "pivot": [1, 1]},
            "Z": {"blocks": [(0, 0), (1, 0), (1, 1), (2, 1)], "pivot": [1, 1]},
        }

        self.next_piece = random.choice(list(self.pieces.keys()))
        self.current_piece = self.next_piece
        self.stored_piece = ""

        self.Clock = pygame.time.Clock()
        self.fps = 24
        self.drop_speed = 1000
        self.move_delay = self.drop_speed
        self.move_timer = 0
        self.total_line_cleared = 0
        self.score = 0
        self.death = 0
        self.ui_instance = UI(self.total_line_cleared, self.score) if UI else None

        self.board_size = (10, 20)
        self.board: List[List[CellType]] = self.ConstructBoard()
        self.current_pivot: List[float] = [0.0, 0.0]

    def ConstructBoard(self) -> List[List[CellType]]:
        return [
            ["" for _ in range(self.board_size[0])] for _ in range(self.board_size[1])
        ]

    def GetActives(self) -> List[Tuple[int, int, str]]:
        active_blocks: List[Tuple[int, int, str]] = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                cell = self.board[row][col]
                if isinstance(cell, tuple) and cell[1]:
                    active_blocks.append((row, col, cell[0]))
        return active_blocks

    def LockPiece(self, active_blocks: List[Tuple[int, int, str]]):
        if self.debug:
            console.log("INFO", f"Locking {self.current_piece}")
        for row, col, piece_name in active_blocks:
            self.board[row][col] = (piece_name, False)
        self.CreatePiece()
        self.LineClear()

    def Gravity(self):
        active_blocks = self.GetActives()
        if not active_blocks:
            return

        for row, col, _ in active_blocks:
            if row + 1 >= self.board_size[1]:
                self.LockPiece(active_blocks)
                return
            target = self.board[row + 1][col]
            if not self.god_mode and isinstance(target, tuple) and target[1] is False:
                self.LockPiece(active_blocks)
                return

        active_blocks.sort(key=lambda x: x[0], reverse=True)
        for row, col, piece_name in active_blocks:
            self.board[row][col] = ""
            self.board[row + 1][col] = (piece_name, True)
        self.current_pivot[0] += 1

    def Movement(self, dir: int):
        active_blocks = self.GetActives()
        if not active_blocks:
            return
        for row, col, _ in active_blocks:
            new_col = col + dir
            if new_col < 0 or new_col >= self.board_size[0]:
                return
            target = self.board[row][new_col]
            if not self.god_mode and isinstance(target, tuple) and target[1] is False:
                return

        active_blocks.sort(key=lambda x: x[1], reverse=(dir == 1))
        for row, col, piece_name in active_blocks:
            self.board[row][col] = ""
            self.board[row][col + dir] = (piece_name, True)
        self.current_pivot[1] += dir

    def Rotate(self):
        active_blocks = self.GetActives()
        if not active_blocks: return

        pivit_row, pivit_col = self.current_pivot
        
        for offset_row, offset_col in [(0, 0), (0, 1), (0, -1), (0, 2), (0, -2)]:
            new_positions = []
            possible = True
            
            for row, col, name in active_blocks:
                dir_row, dir_col = row - pivit_row, col - pivit_col
                new_row = int(pivit_row + dir_col) + offset_row
                new_col = int(pivit_col - dir_row) + offset_col

                if not (0 <= new_row < self.board_size[1] and 0 <= new_col < self.board_size[0]):
                    possible = False
                    break
                
                target = self.board[new_row][new_col]
                if not self.god_mode and isinstance(target, tuple) and target[1] is False:
                    possible = False
                    break
                new_positions.append((new_row, new_col, name))

            if possible:
                for row, col, _ in active_blocks:
                    self.board[row][col] = ""
                for row, col, name in new_positions:
                    self.board[row][col] = (name, True)
                self.current_pivot[0] += offset_row
                self.current_pivot[1] += offset_col
                return
                
        if self.debug:
            console.log("WARN", "Rotation Blocked: No valid kick position found")

    def CreatePiece(self):
        piece_name = self.next_piece
        self.current_piece = piece_name
        self.next_piece = random.choice(list(self.pieces.keys()))
        data = self.pieces[piece_name]
        x_offset = self.board_size[0] // 2 - 1

        if self.debug:
            console.log("NOTICE", f"Spawning: {piece_name}")

        for row, col in data["blocks"]:
            if not self.god_mode and self.board[row][col + x_offset] != "":
                self.death += 1
                if self.death > 50:
                    self.running = False
                    return
            self.board[row][col + x_offset] = (piece_name, True)

        self.current_pivot = [
            float(data["pivot"][0]),
            float(data["pivot"][1] + x_offset),
        ]

    def LoadStorePiece(self):
        if self.stored_piece != "":
            self.next_piece, self.stored_piece = self.stored_piece, self.current_piece
        else:
            self.stored_piece = self.current_piece
            self.next_piece = random.choice(list(self.pieces.keys()))

        for row, col, _ in self.GetActives():
            self.board[row][col] = ""
        self.CreatePiece()

    def LineClear(self):
        row = len(self.board) - 1
        cleared = 0
        while row >= 0:
            full = all(cell != "" and not cell[1] for cell in self.board[row])
            if full:
                del self.board[row]
                self.board.insert(0, ["" for _ in range(self.board_size[0])])
                cleared += 1
                self.total_line_cleared += 1
            else:
                row -= 1
        if cleared > 0:
            self.score += self.CalculateScore(cleared)
            if self.debug:
                console.log("SUCCESS", f"Cleared {cleared} lines. Score: {self.score}")

    def CalculateScore(self, lines: int):
        level = self.total_line_cleared // 10
        scores = {1: 40, 2: 100, 3: 300, 4: 1200}
        return scores.get(lines, 0) * (level + 1)

    def CheckEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    console.log(
                        "NOTICE", "Game Paused" if self.paused else "Game Resumed"
                    )

                if event.key == pygame.K_d:
                    self.debug = not self.debug
                    console.log("SUCCESS", f"Debug logging: {self.debug}")

                if event.key == pygame.K_g:
                    self.god_mode = not self.god_mode
                    console.log("CRITICAL", f"God Mode: {self.god_mode}")

                if event.key == pygame.K_BACKSPACE:
                    self.board = self.ConstructBoard()
                    self.CreatePiece()
                    console.log("WARN", "Board Cleared manually")

                if event.key == pygame.K_PERIOD:
                    self.drop_speed = max(50, self.drop_speed - 100)
                    self.move_delay = self.drop_speed
                    console.log("DEBUG", f"Drop Speed: {self.drop_speed}ms")

                if event.key == pygame.K_COMMA:
                    self.drop_speed += 100
                    self.move_delay = self.drop_speed
                    console.log("DEBUG", f"Drop Speed: {self.drop_speed}ms")

                if not self.paused:
                    if event.key == pygame.K_LEFT:
                        self.Movement(-1)
                    if event.key == pygame.K_RIGHT:
                        self.Movement(1)
                    if event.key == pygame.K_UP:
                        self.Rotate()
                    if event.key == pygame.K_SPACE:
                        self.LoadStorePiece()
                    if event.key == pygame.K_DOWN:
                        self.move_delay = self.drop_speed / 10

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.move_delay = self.drop_speed

    def Loop(self):
        console.header("STARTING TETRIS DEBUG SESSION")
        self.CreatePiece()
        while self.running:
            dt = self.Clock.tick(self.fps)
            self.screen.fill(self.BGC)

            self.CheckEvents()

            if not self.paused and self.death < 1:
                self.move_timer += dt
                if self.move_timer >= self.move_delay:
                    self.Gravity()
                    self.move_timer = 0

            if self.ui_instance:
                self.ui_instance.UpdateText(self.total_line_cleared, self.score)
                self.ui_instance.DrawBoard(
                    self.board,
                    self.screen,
                    self.next_piece,
                    self.stored_piece,
                    self.pieces,
                )

            if self.paused:
                overlay = pygame.Surface(self.ASPECTS_SCREEN, pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 100))
                self.screen.blit(overlay, (0, 0))

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.Loop()
