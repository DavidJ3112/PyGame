import pygame

class UI:
    def __init__(self, screen) -> None:
        pass

    def DrawBoard(self, board, screen):
        width, height = screen.get_size()
        CELL_SIZE = height // 25
        pw, ph = CELL_SIZE * 10, CELL_SIZE * 20 
        px, py = (width // 2) - (pw // 2), (height // 2) - (ph // 2) + 40
        
        hud_elements = [
            # Main Playfield (The "Well")
            ((px, py, pw, ph), (0, 0, 0), 0),                                      # Inner black background
            ((px - 5, py - 5, pw + 10, ph + 10), (255, 255, 255), 5),              # White border/frame

            # "Next" Piece Display (Positioned to the right)
            ((px + pw + 20, py + 50, CELL_SIZE * 4, CELL_SIZE * 4), (0, 0, 0), 0), # Inner black background
            ((px + pw + 15, py + 45, (CELL_SIZE * 4) + 10, (CELL_SIZE * 4) + 10), (255, 255, 255), 3), # White border

            # Sidebar / Stats Box (Positioned to the left)
            ((px - 160, py, 140, 60), (0, 0, 0), 0),                              # Inner black background (e.g., Score/Level)
            ((px - 165, py - 5, 150, 70), (255, 255, 255), 3),                    # White border

            # Top Header Box (Positioned above the playfield)
            ((px, py - 80, pw, 50), (0, 0, 0), 0),                                # Inner black background (e.g., Lines count)
            ((px - 5, py - 85, pw + 10, 60), (255, 255, 255), 3)                  # White border
        ]
                
        
        screen.fill((50, 50, 50)) 

        for rect, color, thickness in hud_elements:
            pygame.draw.rect(screen, color, rect, thickness)
        
        Board_Elements = []
        for row in range(len(board)):
            for col in range(len(board[row])):
                x = px + col * CELL_SIZE
                y = py + row * CELL_SIZE

                TETRIS_COLORS = {
                    "I": (0, 255, 255),   # Cyan
                    "O": (255, 255, 0),   # Yellow
                    "T": (170, 0, 255),   # Purple
                    "S": (0, 255, 0),     # Green
                    "Z": (255, 0, 0),     # Red
                    "J": (0, 0, 255),     # Blue
                    "L": (255, 136, 0),   # Orange
                }

                cell = board[row][col]

                if cell == '':
                    Board_Elements.append(((x, y, CELL_SIZE, CELL_SIZE), (0,0,0)))
                else:
                    try:
                        piece_name, is_active = cell
                        Board_Elements.append(((x, y, CELL_SIZE, CELL_SIZE), TETRIS_COLORS[piece_name]))
                    except:
                        raise KeyError(f"Invalid piece identifier: {piece_name}")


        
        for rect, color in Board_Elements:
            pygame.draw.rect(screen, color, rect)
                