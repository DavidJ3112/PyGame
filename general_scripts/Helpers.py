from ANSI import ANSI
import itertools
import datetime
import time
import sys

class console:

    @staticmethod
    def log(level, message):
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        colors: dict = {
            "INFO": ANSI.CYAN,
            "ERROR": ANSI.RED,
            "WARN": ANSI.YELLOW,
            "SUCCESS": ANSI.GREEN,
        }

        color = colors.get(level, "")
        print(f"{color}[{time}] {level}: {message}{ANSI.RESET}")

    @staticmethod
    def ask(prompt: str) -> str:
        return input(ANSI.wrap(prompt + " > ", ANSI.BLUE, ANSI.BOLD))

    @staticmethod
    def confirm(prompt: str) -> bool:
        res = input(ANSI.wrap(f"{prompt} (y/n): ", ANSI.YELLOW)).lower()
        return res in ("y", "yes")

    @staticmethod
    def progress_bar(total=20, delay=0.05):
        for i in range(total + 1):
            bar = "█" * i + "-" * (total - i)
            print(f"\r{ANSI.CYAN}[{bar}]{ANSI.RESET}", end="", flush=True)
            time.sleep(delay)
        print()

    @staticmethod
    def spinner(stop_event, text="Loading...", delay=0.1):
        for char in itertools.cycle("|/-\\"):
            if stop_event.is_set():
                break
            sys.stdout.write(f"\r{text} {char}")
            sys.stdout.flush()
            time.sleep(delay)
        print("\r" + " " * (len(text) + 2), end="\r")

if __name__ == "__main__":
    console.log("WARN","Death")