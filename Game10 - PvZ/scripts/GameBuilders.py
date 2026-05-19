import sys, os

parent_dir = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)
sys.path.append(parent_dir)

from init import *


class Constructions:
    @staticmethod
    def ConstructBoard(game):
        if 1 <= game.current_level <= 10:
            game.current_lawn = "normal"
        elif 11 <= game.current_level <= 20:
            game.current_lawn = "night"
        elif 21 <= game.current_level <= 30:
            game.current_lawn = "pool"
        elif 31 <= game.current_level <= 40:
            game.current_lawn = "fog"
        elif 41 <= game.current_level <= 50:
            game.current_lawn = "roof"
        else:
            game.current_lawn = "glitched"

        game.rows, game.cols = game.lawn_size[game.current_lawn]

        mx, my = 60, 80
        sw, sh = game.screen.get_size()

        cell = min((sw - 2 * mx) // game.cols, (sh - 2 * my) // game.rows)

        game.cell_size = (cell, cell)

        grid_w, grid_h = game.cols * cell, game.rows * cell

        game.lawn_offset = (
            (sw - grid_w) // 2,
            (sh - grid_h) // 2 + 20,
        )

        lawn = []

        rows, cols = game.lawn_size[game.current_lawn]
        props = game.lawn_properties[game.current_lawn]

        night = props["night"]
        watered_rows = props["watered_rows"]
        watered_cols = props["watered_cols"]
        watered_tiles = props["watered_tiles"]
        tilted_rows = props["tilted_rows"]
        tilted_cols = props["tilted_cols"]
        tilted_tiles = props["tilted_tiles"]
        tile_skin = props["tile_skin"]

        for r in range(rows):
            row = []
            for c in range(cols):
                is_watered = (
                    r in watered_rows or c in watered_cols or (c, r) in watered_tiles
                )
                is_tilted = (
                    r in tilted_rows or c in tilted_cols or (c, r) in tilted_tiles
                )

                if is_watered:
                    row.append(
                        ((c, r), "water", "tilted" if is_tilted else "", "empty")
                    )
                else:
                    row.append(
                        ((c, r), tile_skin, "tilted" if is_tilted else "", "empty")
                    )

            lawn.append(row)

        game.game_lawn = {"Game_Grid": lawn, "night": night}
