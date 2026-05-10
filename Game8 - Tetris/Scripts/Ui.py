import pygame

class UI:
    def __init__(self, total_line_cleared, score) -> None:
        pygame.font.init()
        self.font = pygame.font.SysFont("consolas", 28)
        self.small_font = pygame.font.SysFont("consolas", 20)
        self.debug_font = pygame.font.SysFont("consolas", 16, bold=True)
        self.total_line_cleared = total_line_cleared
        self.score = score

    def UpdateText(self, total_line_cleared, score):
        self.total_line_cleared = total_line_cleared
        self.score = score

    def DrawBoard(self, board, screen, next_piece, stored_piece, pieces, debug_info=None):
        """
        Modified to accept debug_info: 
        Expected dict: {"paused": bool, "god_mode": bool, "debug": bool}
        """
        width, height = screen.get_size()
        CELL_SIZE = height // 25
        pw, ph = CELL_SIZE * 10, CELL_SIZE * 20 
        px, py = (width // 2) - (pw // 2), (height // 2) - (ph // 2) + 40
        
        hud_elements = [
            # Main Playfield (The "Well")
            ((px, py, pw, ph), (0, 0, 0), 0),                                     
            ((px - 5, py - 5, pw + 10, ph + 10), (255, 255, 255), 5),              

            # "Next" Piece Display
            ((px + pw + 20, py + 50, CELL_SIZE * 4, CELL_SIZE * 4), (0, 0, 0), 0), 
            ((px + pw + 15, py + 45, (CELL_SIZE * 4) + 10, (CELL_SIZE * 4) + 10), (255, 255, 255), 3), 

            # "Stored" Piece Display
            ((px + pw + 20, py + 200, CELL_SIZE * 4, CELL_SIZE * 4), (0, 0, 0), 0), 
            ((px + pw + 15, py + 195, (CELL_SIZE * 4) + 10, (CELL_SIZE * 4) + 10), (255, 255, 255), 3), 

            # Sidebar / Stats Box
            ((px - 160, py, 140, 60), (0, 0, 0), 0),                               
            ((px - 165, py - 5, 150, 70), (255, 255, 255), 3),                    

            # Top Header Box
            ((px, py - 80, pw, 50), (0, 0, 0), 0),                                
            ((px - 5, py - 85, pw + 10, 60), (255, 255, 255), 3)                  
        ]
        
        screen.fill((50, 50, 50)) 

        for rect, color, thickness in hud_elements:
            pygame.draw.rect(screen, color, rect, thickness)
        
        TETRIS_COLORS = {
            "I": (0, 255, 255), "O": (255, 255, 0), "T": (170, 0, 255),
            "S": (0, 255, 0), "Z": (255, 0, 0), "J": (0, 0, 255),
            "L": (255, 136, 0), "Clear": (255, 255, 255),
        }

        # Draw main board pieces
        for row in range(len(board)):
            for col in range(len(board[row])):
                cell = board[row][col]
                if cell != '':
                    x = px + col * CELL_SIZE
                    y = py + row * CELL_SIZE
                    piece_name = cell[0] if isinstance(cell, tuple) else cell
                    color = TETRIS_COLORS.get(piece_name, (200, 200, 200))
                    pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

        # Draw grid lines
        for row in range(21):
            y = py + row * CELL_SIZE
            pygame.draw.line(screen, (40, 40, 40), (px, y), (px + pw, y))
        for col in range(11):
            x = px + col * CELL_SIZE
            pygame.draw.line(screen, (40, 40, 40), (x, py), (x, py + ph))

        # Draw HUD labels and data
        self.DrawText(screen, "SCORE", (px - 145, py + 5), small=True)
        self.DrawText(screen, str(self.score), (px - 145, py + 30))
        self.DrawText(screen, "LINES", (px + 10, py - 75), small=True)
        self.DrawText(screen, str(self.total_line_cleared), (px + 110, py - 75))
        self.DrawText(screen, "NEXT", (px + pw + 35, py + 10), small=True)
        self.DrawText(screen, "HOLD", (px + pw + 35, py + 160), small=True)

        # Draw Preview Pieces
        self.DrawBoxedPiece(screen, next_piece, pieces, px, py, pw, CELL_SIZE, 0)
        self.DrawBoxedPiece(screen, stored_piece, pieces, px, py, pw, CELL_SIZE, 150)

        # --- DEBUG OVERLAYS ---
        if debug_info:
            if debug_info.get("paused"):
                self.DrawDebugLabel(screen, "PAUSED", (px + (pw//2) - 40, py + (ph//2)), (255, 50, 50))
            if debug_info.get("god_mode"):
                self.DrawDebugLabel(screen, "GOD MODE", (px - 160, py + 100), (255, 215, 0))
            if debug_info.get("debug"):
                self.DrawDebugLabel(screen, "LOGGING ACTIVE", (px - 160, py + 130), (50, 255, 50))

    def DrawDebugLabel(self, screen, text, pos, color):
        surface = self.debug_font.render(text, True, color)
        # Add a small shadow/border for readability
        bg_rect = surface.get_rect(topleft=pos).inflate(10, 4)
        pygame.draw.rect(screen, (20, 20, 20), bg_rect)
        pygame.draw.rect(screen, color, bg_rect, 1)
        screen.blit(surface, pos)

    def DrawText(self, screen, text, pos, color=(255, 255, 255), small=False):
        font = self.small_font if small else self.font
        surface = font.render(text, True, color)
        screen.blit(surface, pos)
    
    def DrawBoxedPiece(self, screen, piece_name, pieces, px, py, pw, CELL_SIZE, Y_Offset):
        if piece_name == "" or piece_name not in pieces:
            return

        TETRIS_COLORS = {
            "I": (0, 255, 255), "O": (255, 255, 0), "T": (170, 0, 255),
            "S": (0, 255, 0), "Z": (255, 0, 0), "J": (0, 0, 255),
            "L": (255, 136, 0),
        }

        box_x, box_y = px + pw + 20, py + 50 + Y_Offset
        box_size = CELL_SIZE * 4
        piece = pieces[piece_name]["blocks"]
        color = TETRIS_COLORS.get(piece_name, (255, 255, 255))

        min_x = min(x for x, y in piece)
        min_y = min(y for x, y in piece)
        max_x = max(x for x, y in piece)
        max_y = max(y for x, y in piece)

        piece_w = (max_x - min_x + 1)
        piece_h = (max_y - min_y + 1)

        offset_x = box_x + (box_size - piece_w * CELL_SIZE) // 2
        offset_y = box_y + (box_size - piece_h * CELL_SIZE) // 2

        for x, y in piece:
            pygame.draw.rect(screen, color, (
                offset_x + (x - min_x) * CELL_SIZE,
                offset_y + (y - min_y) * CELL_SIZE,
                CELL_SIZE, CELL_SIZE
            ))