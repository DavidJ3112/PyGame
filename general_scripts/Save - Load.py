from ANSI import ANSI
import json
import os

class SaveLoad:
    @staticmethod
    def save(save_file, data, log=False):
        if log: print(ANSI.wrap(f"{data} Has Been Saved to: {save_file}", ANSI.YELLOW, ANSI.BOLD))

        os.makedirs(os.path.dirname(save_file), exist_ok=True)
        with open(save_file, "w") as f:
            json.dump(data, f)

    @staticmethod
    def load(save_file, log=False):
        if not os.path.exists(save_file):
            if log: print(ANSI.wrap(f"Save Not Found: {save_file}", ANSI.RED, ANSI.BOLD))
            return None
        with open(save_file, "r") as f:
            if log: print(ANSI.wrap(f"Save Found: {save_file}", ANSI.GREEN, ANSI.BOLD))
            return json.load(f)

    @staticmethod
    def get_save_path(slot):
        return os.path.join(
            os.path.dirname(__file__),
            "Save",
            f"data_{slot}.json"
        )


#!^ multi save
if __name__ == "__main__":
    print(SaveLoad.load(SaveLoad.get_save_path(1)))
    print(SaveLoad.load(SaveLoad.get_save_path(2)))
    print(SaveLoad.load(SaveLoad.get_save_path(3)))
    
    SaveLoad.save(SaveLoad.get_save_path(1), {"name": "Rose", "age": 18})
    SaveLoad.save(SaveLoad.get_save_path(2), {"name": "Bob", "age": 25})
    SaveLoad.save(SaveLoad.get_save_path(3), {"name": "Eve", "age": 30})

#!^ Single save file
if __name__ != "__main__":
    data = {"name": "Rose", "age": 18, "level": 24}

    file_location = os.path.join(os.path.dirname(__file__), "Save", "data.json")

    SaveLoad.save(file_location, data)

    data_loaded = SaveLoad.load(file_location)
    print(data_loaded)