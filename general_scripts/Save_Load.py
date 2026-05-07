try:
    from ANSI import ANSI
    from Helpers import console
except ImportError:
    from .ANSI import ANSI
    from .Helpers import console

import json
import sys
import os

class SaveLoad:
    """Advanced JSON save system with safety checks and flexible confirmation support."""

    @staticmethod
    def _ensure_path(save_file):
        """
        Internal check to ensure the directory for a file exists.
        Args:
            save_file (str): The path to check/create.
        Returns:
            bool: True if path is valid or created, False if directory creation fails.
        """
        try:
            directory = os.path.dirname(save_file)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            return True
        except Exception as e:
            console.log("ERROR", f"Could not create directory path: {e}")
            return False

    @staticmethod
    def save(save_file, data, log=False):
        """
        Forces a save, overwriting any existing file without warning.
        Args:
            save_file (str): Full path to the destination file.
            data (dict/list): Data to be serialized.
            log (bool): If True, logs success to console.
        """
        if not SaveLoad._ensure_path(save_file):
            return

        try:
            with open(save_file, "w") as f:
                json.dump(data, f, indent=4)
            if log:
                console.log("SUCCESS", f"Data saved to {os.path.basename(save_file)}")
        except Exception as e:
            console.log("ERROR", f"Failed to save file: {e}")

    @staticmethod
    def safe_save(save_file, data, callback=None):
        """
        Saves data with an overwrite warning. Supports custom UI callbacks for Pygame.
        Args:
            save_file (str): Full path to the destination file.
            data (dict/list): Data to be serialized.
            callback (function): Optional. A function that returns True/False (e.g., a Pygame pop-up).
        """
        if os.path.exists(save_file):
            filename = os.path.basename(save_file)
            warn_msg = f"Save file '{filename}' already exists. Overwrite?"
            
            if callback:
                if not callback(warn_msg):
                    return False
            else:
                if not console.confirm(warn_msg):
                    console.log("INFO", "Save aborted by user.")
                    return False
        
        SaveLoad.save(save_file, data, log=True)
        return True

    @staticmethod
    def load(save_file, log=False):
        """
        Loads data from a JSON file. Logs an error if the path/file is missing.
        Args:
            save_file (str): Full path to the file.
            log (bool): If True, logs success to console.
        Returns:
            dict/list: Parsed JSON data or None if failed.
        """
        if not os.path.exists(save_file):
            console.log("ERROR", f"Save file not found at: {save_file}")
            return None

        try:
            with open(save_file, "r") as f:
                data = json.load(f)
            if log:
                console.log("SUCCESS", f"Loaded data from {os.path.basename(save_file)}")
            return data
        except Exception as e:
            console.log("ERROR", f"Failed to load JSON: {e}")
            return None

    @staticmethod
    def get_save_path(slot=1, name: str="") -> str:
        """
        Generates an absolute path for a specific save slot.
        Args:
            slot (int/str): The save slot identifier.
            name (str): The name prefix of the save.
        Returns:
            str: The full path to the slot's JSON file.
        """
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        prefix = name if name != "" else "Save"
        return os.path.join(base_dir, "Content", "Saves", f"{prefix}_{slot}.json")

def my_pygame_popup(message):
    return console.confirm("Over Write")

if __name__ == "__main__":
    path = SaveLoad.get_save_path(1, "HeroData")
    data = {"hp": 100, "gold": 50}

    SaveLoad.safe_save(path, data, callback=my_pygame_popup)