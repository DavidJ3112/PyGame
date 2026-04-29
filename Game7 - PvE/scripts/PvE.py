import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))

sys.path.append(parent_dir)

from general_scripts.ANSI import ANSI

class PvE:
    def __init__(self):
        pass

    def Attack(self):
        return True, "Attack"

    def Guard(self):
        return True, "Guard"

    def Item(self):
        return False, "Item"

    def Flee(self):
        return True, "Flee"
