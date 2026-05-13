from typing import Any, Callable, Union, Optional
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import base64
import json
import sys
import os

try:
    from Helpers import console
except ImportError:
    from .Helpers import console


class SaveLoad:
    """
    Save system with optional encryption.
    Config files are plain JSON, game saves are encrypted.
    """

    # ---------------- KEY GENERATION ----------------

    @staticmethod
    def generate_key_from_string(password: str) -> bytes:
        """
        Generates a 32-byte Fernet key from a string.

        Args:
            password (str): The password string to derive the key from.

        Returns:
            bytes: A URL-safe base64-encoded key.
        """
        password_bytes = password.encode()
        salt = b"pygame_salt_"

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )

        return base64.urlsafe_b64encode(kdf.derive(password_bytes))

    # ---------------- PATH HANDLING ----------------

    @staticmethod
    def _ensure_path(save_file: str) -> bool:
        """
        Creates directory folders if they do not exist.

        Args:
            save_file (str): The full destination file path.

        Returns:
            bool: True if path exists or was created, False on failure.
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
    def get_save_path(
        slot: Union[int, str] = 0,
        name: str = "Save",
        folder_type: str = "saves"
    ) -> str:
        """
        Constructs a path for save or config files.

        Args:
            slot (Union[int, str]): Slot number or identifier. Use 0 for no slot.
            name (str): The base name of the file.
            folder_type (str): Subfolder name (e.g., 'save', 'config').

        Returns:
            str: The absolute path to the file.
        """
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        try:
            sub_folder = folder_type.capitalize()

            if slot != 0:
                return os.path.join(
                    base_dir, "Content", sub_folder, f"{name}_{slot}.json"
                )

            return os.path.join(
                base_dir, "Content", sub_folder, f"{name}.json"
            )

        except Exception as e:
            raise SyntaxError(f"Path generation failed: {e}")

    # ---------------- SAVE ----------------

    @staticmethod
    def save(
        save_file: str,
        data: Any,
        key: Optional[bytes] = None,
        encrypt: bool = False,
        log: bool = False
    ) -> None:
        """
        Serializes data to JSON and writes it to disk.

        Args:
            save_file (str): Target file path.
            data (Any): Serializable data to save.
            key (Optional[bytes]): Encryption key.
            encrypt (bool): Whether to use Fernet encryption.
            log (bool): If True, logs success message to console.
        """
        if not SaveLoad._ensure_path(save_file):
            return

        try:
            json_str = json.dumps(data)

            if encrypt and key is not None:
                fernet = Fernet(key)
                output = fernet.encrypt(json_str.encode("utf-8"))
            else:
                output = json_str.encode("utf-8")

            with open(save_file, "wb") as f:
                f.write(output)

            if log:
                console.log("SUCCESS", f"Saved {os.path.basename(save_file)}")

        except Exception as e:
            console.log("ERROR", f"Failed to save file: {e}")

    # ---------------- SAFE SAVE ----------------

    @staticmethod
    def safe_save(
        save_file: str,
        data: Any,
        key: Optional[bytes] = None,
        encrypt: bool = False,
        callback: Optional[Callable[[str], bool]] = None,
    ) -> bool:
        """
        Saves data while prompting for confirmation if file exists.

        Args:
            save_file (str): Target file path.
            data (Any): Serializable data to save.
            key (Optional[bytes]): Encryption key.
            encrypt (bool): Whether to use Fernet encryption.
            callback (Optional[Callable]): Custom UI function for confirmation.

        Returns:
            bool: True if saved successfully, False if aborted or failed.
        """
        if os.path.exists(save_file):
            filename = os.path.basename(save_file)
            msg = f"Save file '{filename}' already exists. Overwrite?"

            if callback:
                if not callback(msg):
                    console.log("INFO", "Save aborted by user.")
                    return False
            else:
                if not console.confirm(msg):
                    console.log("INFO", "Save aborted by user.")
                    return False

        SaveLoad.save(save_file, data, key, encrypt=encrypt, log=True)
        return True

    # ---------------- LOAD ----------------

    @staticmethod
    def load(
        save_file: str,
        key: Optional[bytes] = None,
        encrypted: bool = False,
        log: bool = False
    ) -> Optional[Any]:
        """
        Reads and deserializes a file from disk.

        Args:
            save_file (str): Path of the file to load.
            key (Optional[bytes]): Decryption key.
            encrypted (bool): Whether the file is encrypted.
            log (bool): If True, logs success message to console.

        Returns:
            Optional[Any]: The loaded data, or None if loading fails.
        """
        if not os.path.exists(save_file):
            console.log("ERROR", f"Save file not found at: {save_file}")
            return None

        try:
            with open(save_file, "rb") as f:
                raw = f.read()

            if encrypted and key is not None:
                fernet = Fernet(key)
                json_str = fernet.decrypt(raw).decode("utf-8")
            else:
                json_str = raw.decode("utf-8")

            data = json.loads(json_str)

            if log:
                console.log("SUCCESS", f"Loaded {os.path.basename(save_file)}")

            return data

        except Exception as e:
            console.log("ERROR", f"Failed to load JSON: {e}")
            return None


# ---------------- TEST ----------------

if __name__ == "__main__":

    def my_pygame_popup(message: str) -> bool:
        return console.confirm(message)

    game_key = SaveLoad.generate_key_from_string("Example")

    # -------- GAME SAVE (ENCRYPTED) --------
    path = SaveLoad.get_save_path(5, "HeroData")

    SaveLoad.safe_save(
        path,
        {"hp": 100, "gold": 50},
        key=game_key,
        encrypt=True,
        callback=my_pygame_popup
    )

    # -------- GAME LOAD --------
    print(SaveLoad.load(path, game_key, encrypted=True, log=True))

    # -------- CONFIG (NOT ENCRYPTED) --------
    config_path = SaveLoad.get_save_path(0, "Config", "Configs")

    SaveLoad.save(
        config_path,
        {"volume": 50},
        encrypt=False,
        log=True
    )

    print(SaveLoad.load(config_path, encrypted=False, log=True))