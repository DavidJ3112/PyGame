try:
    from ANSI import ANSI
except ImportError:
    from .ANSI import ANSI
import itertools
import datetime
import time
import sys
import os
import re

class console():
    """A static utility class for formatted console output, input, and file logging."""
    
    _entry_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    LOG_DIR = os.path.join(_entry_dir, "Content", "Logs")
    
    _ts = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")[:-3]
    LOG_FILE = os.path.join(LOG_DIR, f"Game_log_({_ts}).log")
    
    _cleaned_up = False
    MAX_LOG_FILES = 5

    @classmethod
    def set_max_logs(cls, count: int):
        """
        Sets the maximum number of log files to keep in the directory.
        Args:
            count (int): The number of recent logs to retain.
        """
        cls.MAX_LOG_FILES = count

    @staticmethod
    def _prepare_log_system():
        """Creates the log directory and prunes old log files to stay under the limit."""
        if not os.path.exists(console.LOG_DIR):
            os.makedirs(console.LOG_DIR, exist_ok=True)
        
        if not console._cleaned_up:
            try:
                files = [os.path.join(console.LOG_DIR, f) for f in os.listdir(console.LOG_DIR) if f.endswith(".log")]
                if len(files) >= console.MAX_LOG_FILES:
                    files.sort(key=os.path.getmtime)
                    to_delete = len(files) - console.MAX_LOG_FILES + 1
                    for i in range(to_delete):
                        os.remove(files[i])
                console._cleaned_up = True
            except Exception:
                pass

    @staticmethod
    def _strip_ansi(text):
        """
        Removes ANSI escape sequences from a string for clean text file storage.
        Args:
            text (str): The string containing ANSI codes.
        Returns:
            str: The sanitized plain-text string.
        """
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    @staticmethod
    def save_to_file(message):
        """
        Appends a sanitized message to the current session's log file.
        Args:
            message (str): The string to write to the file.
        """
        console._prepare_log_system()
        clean_message = console._strip_ansi(message)
        try:
            with open(console.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(clean_message + "\n")
        except Exception:
            pass

    @staticmethod
    def log(level, message):
        """
        Prints a timestamped, color-coded message and saves it to the log file.
        Args:
            level (str): The severity level (INFO, ERROR, WARN, SUCCESS).
            message (str): The content to log.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        colors = {
            "INFO": ANSI.CYAN,
            "ERROR": ANSI.RED,
            "WARN": ANSI.YELLOW,
            "SUCCESS": ANSI.GREEN,
        }
        color = colors.get(level, "")
        full_msg = f"[{timestamp}] {level}: {message}"
        
        print(f"{color}{full_msg}{ANSI.RESET}")
        console.save_to_file(full_msg)

    @staticmethod
    def ask(prompt: str) -> str:
        """
        Displays a styled prompt and returns the user's string input.
        Args:
            prompt (str): The question or instruction for the user.
        Returns:
            str: The user's input.
        """
        res = input(ANSI.wrap(prompt + " > ", ANSI.BLUE, ANSI.BOLD))
        console.save_to_file(f"[INPUT] {prompt} > {res}")
        return res

    @staticmethod
    def confirm(prompt: str) -> bool:
        """
        Prompts the user for a yes/no confirmation.
        Args:
            prompt (str): The message to confirm.
        Returns:
            bool: True if user inputs 'y' or 'yes', False otherwise.
        """
        res = input(ANSI.wrap(f"{prompt} (y/n): ", ANSI.YELLOW)).lower()
        is_confirmed = res in ("y", "yes")
        console.save_to_file(f"[CONFIRM] {prompt} ({res})")
        return is_confirmed

    @staticmethod
    def spinner(stop_event, text="Loading...", delay=0.1):
        """
        Displays a visual terminal spinner on a single line until an event is set.
        Args:
            stop_event (threading.Event): The signal to stop the spinner.
            text (str): Text to display alongside the spinner.
            delay (float): Seconds between frame updates.
        """
        for char in itertools.cycle("|/-\\"):
            if stop_event.is_set():
                break
            sys.stdout.write(f"\r{text} {char}")
            sys.stdout.flush()
            time.sleep(delay)
        print("\r" + " " * (len(text) + 2), end="\r")

if __name__ == "__main__":
    console.log("INFO", f"Logs will save relative to the launcher: {console.LOG_DIR}")