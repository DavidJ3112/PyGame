import pygame

class UI:
    def __init__(self, screen) -> None:
        pass

    def DrawBoard(self, board, screen):
        width, height = screen.get_size()
        cell_size = height // 25
        pw, ph = cell_size * 10, cell_size * 20 
        px, py = (width // 2) - (pw // 2), (height // 2) - (ph // 2) 
        
        hud_elements = [
            ((px, py, pw, ph), (0, 0, 0), 0),
            ((px - 5, py - 5, pw + 10, ph + 10), (255, 255, 255), 5),
            ((px + pw + 20, py + 50, cell_size * 4, cell_size * 4), (0, 0, 0), 0),
            ((px + pw + 15, py + 45, (cell_size * 4) + 10, (cell_size * 4) + 10), (255, 255, 255), 3),
            ((px - 160, py, 140, 60), (0, 0, 0), 0),
            ((px - 165, py - 5, 150, 70), (255, 255, 255), 3),
            ((px, py - 80, pw, 50), (0, 0, 0), 0),
            ((px - 5, py - 85, pw + 10, 60), (255, 255, 255), 3)
        ]
        
        
        screen.fill((50, 50, 50)) 

        for rect, color, thickness in hud_elements:
            pygame.draw.rect(screen, color, rect, thickness)