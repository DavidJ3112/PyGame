import time

class DebugPrinter:
    def __init__(self):
        pass
    def debug_info(self, debug_type):
        if debug_type == "ALL":
            RESET = "\033[0m"
            def field(color, label, value, width=None):
                if width is not None:
                    value = f"{value:{width}}"
                return f"{color}{label}: {value}{RESET}"
            debug_text = (
                field("\033[37m", "Pos", f"({self.x:5.0f}, {self.y:5.0f})") + "  " +
                field("\033[36m", "Vel Y", f"{self.vel_y:7.2f}") + "  " +
                field("\033[33m", "Gravity", self.gravity_state) + "  " +
                field("\033[34m", "Camera", f"({self.camera_x:5.0f}, {self.camera_y:5.0f})") + "  " +
                field("\033[35m", "Wallhit", self.wallhit) + "  " +
                field("\033[31m", "Collision", self.collision_result)
            )
            time.sleep(1 / self.FPS)
            print(debug_text)