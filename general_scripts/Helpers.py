import itertools
import datetime
import time
import sys
import os
import re

try:
    from ANSI import ANSI
except ImportError:
    from .ANSI import ANSI

class console():
    """A static utility class for formatted console output, input, and file logging."""
    
    _entry_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    LOG_DIR = os.path.join(_entry_dir, "Content", "Logs")
    _game_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]

    LOG_FILE = None
    MAX_LOG_FILES = 5
    _cleaned_up = False
    _session_history = []

    @classmethod
    def set_max_logs(cls, count: int):
        """
        Sets the maximum number of log files to keep in storage.
        Args:
            count (int): The number of historical log files to retain.
        """
        cls.MAX_LOG_FILES = count

    @staticmethod
    def _prepare_log_system():
        """
        Ensures log directories exist and performs rotation of old log files.
        """
        if not os.path.exists(console.LOG_DIR):
            os.makedirs(console.LOG_DIR, exist_ok=True)

        if console.LOG_FILE is None:
            ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            pid = os.getpid()
            console.LOG_FILE = os.path.join(console.LOG_DIR, f"{console._game_name}_{ts}_PID{pid}.log")
        
        if not console._cleaned_up:
            try:
                files = [os.path.join(console.LOG_DIR, f) for f in os.listdir(console.LOG_DIR) if f.endswith(".log")]
                files.sort(key=os.path.getctime)
                if len(files) > console.MAX_LOG_FILES:
                    for i in range(len(files) - console.MAX_LOG_FILES):
                        if files[i] != console.LOG_FILE:
                            try: os.remove(files[i])
                            except: pass
                console._cleaned_up = True
            except Exception: pass

    @staticmethod
    def _strip_ansi(text):
        """
        Removes ANSI escape codes from string for clean file logging.
        Args:
            text (str): String containing ANSI escape sequences.
        Returns:
            str: Plain text without escape sequences.
        """
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    @staticmethod
    def save_to_file(message: str):
        """
        Appends a message to the log file and cache; restores file if deleted.
        Args:
            message (str): The text message to be saved.
        """
        console._prepare_log_system()
        if console.LOG_FILE is None: return

        clean_message = console._strip_ansi(message)
        console._session_history.append(clean_message)

        try:
            if not os.path.exists(console.LOG_FILE):
                with open(str(console.LOG_FILE), "w", encoding="utf-8") as f:
                    f.write("\n".join(console._session_history) + "\n")
            else:
                with open(str(console.LOG_FILE), "a", encoding="utf-8") as f:
                    f.write(clean_message + "\n")
        except Exception: pass

    @staticmethod
    def log(level, message, time_stamp = True, write_level = True):
        """
        Prints a timestamped, color-coded message to console and saves to log.
        Args:
            level (str): Log severity (TRACE, DEBUG, INFO, SUCCESS, NOTICE, WARN, ERROR, CRITICAL).
            message (str): The message content to log.

            time_stamp (bool): If True, prepends the current timestamp to the message.
            write_level (bool): If True, includes the log level label in the output.
        """

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        colors = {
            "TRACE":    ANSI.YELLOW,       ## Raw data/Packets
            "DEBUG":    ANSI.MAGENTA,      ## Logic flow
            "INFO":     ANSI.CYAN,         ## General status
            "SUCCESS":  ANSI.GREEN,        ## Connections/Handshakes
            "NOTICE":   ANSI.BRIGHT_BLUE,  ## Significant events (e.g., player joined)
            "WARN":     ANSI.YELLOW,       ## Timeouts/Retries
            "ERROR":    ANSI.RED,          ## Socket failures
            "CRITICAL": ANSI.BRIGHT_RED,   ## Server crash/Bind failures
        }
        
        color = colors.get(level.upper(), "")
        
        if time_stamp:
            if write_level:
                full_msg = f"[{timestamp}] {level.upper()}: {message}"
            else:
                full_msg = f"[{timestamp}]: {message}"
        else:
            if write_level:
                full_msg = f"{level.upper()}: {message}"
            else:
                full_msg = f"{message}"
        
        print(f"{color}{full_msg}{ANSI.RESET}")
        
        full_msg = f"[{timestamp}] {level.upper()}: {message}"
        console.save_to_file(full_msg)

    @staticmethod
    def ask(prompt: str) -> str:
        """
        Prompts for user input with formatting and logs the interaction.
        Args:
            prompt (str): The question to display to the user.
        Returns:
            str: The user's input string.
        """

        res = input(ANSI.wrap(prompt + " > ", ANSI.BRIGHT_CYAN, ANSI.BOLD))
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        console.save_to_file(f"[{timestamp}] INPUT: {prompt} > {res}")
        return res

    @staticmethod
    def header(message: str) -> None:
        print(f"{ANSI.CYAN}{ANSI.SAPERATOR}{ANSI.RESET}")
        print(f"{ANSI.CYAN}{message}{ANSI.RESET}")
        print(f"{ANSI.CYAN}{ANSI.SAPERATOR}{ANSI.RESET}")

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        console.save_to_file(f"[{timestamp}] HEADER: {message}")

    @staticmethod
    def confirm(prompt: str) -> bool:
        """
        Prompts for a yes/no confirmation and returns a boolean.
        Args:
            prompt (str): The confirmation message.
        Returns:
            bool: True if user enters 'y' or 'yes', False otherwise.
        """
        res = input(ANSI.wrap(f"{prompt} (y/n): ", ANSI.YELLOW)).lower()
        is_confirmed = res in ("y", "yes")

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        console.save_to_file(f"[{timestamp}] CONFIRM: {prompt} ({res})")
        return is_confirmed

    @staticmethod
    def spinner(stop_event, text="Loading...", delay=0.1):
        """
        Displays an animated text spinner until the stop_event is set.
        Args:
            stop_event (threading.Event): Event used to signal termination.
            text (str): Text to display alongside the spinner.
            delay (float): Seconds to wait between frame updates.
        """
        for char in itertools.cycle("|/-\\"):
            if stop_event.is_set():
                break
            sys.stdout.write(f"\r{text} {char}")
            sys.stdout.flush()
            time.sleep(delay)
        print("\r" + " " * (len(text) + 2), end="\r")