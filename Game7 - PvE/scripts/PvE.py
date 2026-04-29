import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))

sys.path.append(parent_dir)

from general_scripts.ANSI import ANSI

class PvE:
    def __init__(self):
        pass

    def Attack(self, player, enemy):
        print(f"{ANSI.RED} Attack {ANSI.RESET}")
        return

    def Guard(self, player, enemy):
        print(f"{ANSI.RED} Guard {ANSI.RESET}")
        return

    def Flee(self, player, enemy):
        print(f"{ANSI.RED} Flee {ANSI.RESET}")
        return
    
    def Item(self, player, enemy):
        print(f"{ANSI.RED} Inv {ANSI.RESET}")
        return

    def Cast(self, player, enemy, spell_key, spell_data):
        print(f"{ANSI.MAGENTA}Spell: {spell_key}{ANSI.NEW_LINE}Spell Data: {spell_data}{ANSI.RESET}")
    
    def enemy(self):
        print("heheheha")

class Attack_Cycle:
    def boss(self):
        print("boss")

    def normal(self):
        print("boss")
    
    def exp(self):
        print("Level Up")