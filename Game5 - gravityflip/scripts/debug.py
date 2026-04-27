import sys, os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from general_scripts.ANSI import ANSI

class DebugPrinter:
    def __init__(self):
        pass
    def map_info(info):
        print(info)
    def debug_info(self, debug_type):
        RESET = "\033[0m"
        def field(color, label, value, width=None):
            if width is not None:
                value = f"{value:{width}}"
            return f"{color}{label}: {value}{RESET}"
        
        if debug_type == "NONE":
            return

        if debug_type == "ALL":
            debug_text = (
                field(ANSI.WHITE, "Pos", f"({self.x:5.0f}, {self.y:5.0f})") + "  " +
                field(ANSI.CYAN, "Vel Y", f"{self.vel_y:7.2f}") + "  " +
                field(ANSI.YELLOW, "Gravity", self.gravity_state) + "  " +
                field(ANSI.BLUE, "Camera", f"({self.camera_x:5.0f}, {self.camera_y:5.0f})") + "  " +
                field(ANSI.MAGENTA, "Wallhit", self.wallhit) + "  " +
                field(ANSI.RED, "Collision", self.collision_result)
            )

        if debug_type == "SPRITE":
            debug_text = (
                field(ANSI.WHITE, "facing", self.player_facing, width=2) + "  " +
                field(ANSI.CYAN, "movement X", self.player_movement_state_x, width=15) + "  " +
                field(ANSI.CYAN, "movement Y", self.player_movement_state_y, width=15) + "  "
            )


        time.sleep(1 / self.FPS)
        print(debug_text)