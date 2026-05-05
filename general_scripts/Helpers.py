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
    #!^ Resolve path from the LAUNCHED script (importer) rather than this file
    _entry_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    LOG_DIR = os.path.join(_entry_dir, "Content", "Logs")
    
    #!^ Timestamp with milliseconds
    _ts = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")[:-3]
    LOG_FILE = os.path.join(LOG_DIR, f"Game_log_({_ts}).log")
    
    #!^ Track if we have already cleaned up this session
    _cleaned_up = False

    @staticmethod
    def _prepare_log_system():
        #!^ Ensure directory exists
        if not os.path.exists(console.LOG_DIR):
            os.makedirs(console.LOG_DIR, exist_ok=True)
        
        #!^ Only run rotation ONCE per execution to prevent thread-spam
        if not console._cleaned_up:
            try:
                files = [os.path.join(console.LOG_DIR, f) for f in os.listdir(console.LOG_DIR) if f.endswith(".log")]
                #!^ If we are at or over the limit, clear out the oldest
                if len(files) >= console.MAX_LOG_FILES:
                    files.sort(key=os.path.getmtime)
                    #!^ Calculate exactly how many to delete to be under the limit
                    to_delete = len(files) - console.MAX_LOG_FILES + 1
                    for i in range(to_delete):
                        os.remove(files[i])
                console._cleaned_up = True
            except Exception:
                pass

    @staticmethod
    def _strip_ansi(text):
        #!^ Remove ANSI color codes for clean text files
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    @classmethod
    def set_max_logs(cls, count: int):
        cls.MAX_LOG_FILES = count

    @staticmethod
    def save_to_file(message):
        console._prepare_log_system()
        clean_message = console._strip_ansi(message)
        try:
            #!^ Use 'a' for append; threading-friendly
            with open(console.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(clean_message + "\n")
        except Exception:
            pass

    @staticmethod
    def log(level, message):
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
        res = input(ANSI.wrap(prompt + " > ", ANSI.BLUE, ANSI.BOLD))
        console.save_to_file(f"[INPUT] {prompt} > {res}")
        return res

    @staticmethod
    def confirm(prompt: str) -> bool:
        res = input(ANSI.wrap(f"{prompt} (y/n): ", ANSI.YELLOW)).lower()
        is_confirmed = res in ("y", "yes")
        console.save_to_file(f"[CONFIRM] {prompt} ({res})")
        return is_confirmed

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
    console.log("INFO", f"Logs will save relative to the launcher: {console.LOG_DIR}")