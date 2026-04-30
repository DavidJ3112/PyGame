import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))

sys.path.append(parent_dir)

from general_scripts.ANSI import ANSI

class PvE:
    def __init__(self):
        pass

    def Attack(self): PvE.Do_Action(self, "Attack")
    def Guard(self): PvE.Do_Action(self, "Guard")
    def Flee(self): PvE.Do_Action(self, "Flee")
    def Item(self): PvE.Do_Action(self, "Item")
    def Cast(self, spell_key, spell_data): PvE.Do_Action(self, "Spell", (spell_key, spell_data))
    

    def Do_Action(self, mode, spell_data = None):
        Player_Attack_Data = PvE.Player(self, mode, spell_data)
        Enemy_Attack_Data = PvE.Enemy(self)
        PvE.Attack_Cycle(self, Player_Attack_Data, Enemy_Attack_Data)

    def Player(self, mode, spell_data):
        if self.debug:
            print(f"{ANSI.NEW_LINE}{ANSI.BRIGHT_MAGENTA}{ANSI.SAPERATOR}{ANSI.RESET}")
            for key, value in self.player_stats.items():
                print(f"{ANSI.YELLOW}{key}: {value}{ANSI.RESET}")
            print(f"{ANSI.wrap(mode, ANSI.BOLD, ANSI.YELLOW)}")

            if spell_data:
                print(f"{ANSI.NEW_LINE}{ANSI.BRIGHT_MAGENTA}{ANSI.SAPERATOR}{ANSI.RESET}")
                print(f"{ANSI.wrap(str(spell_data), ANSI.BOLD, ANSI.YELLOW)}")
        if mode == "Attack":
            Player_Attack_Data = self.player_stats["atk"]

        elif mode == "Guard":
            Player_Attack_Data = self.player_stats["atk"]

        elif mode == "Flee":
            Player_Attack_Data = self.player_stats["atk"]

        elif mode == "Items":
            Player_Attack_Data = self.player_stats["atk"]

        elif mode == "Spell":
            Player_Attack_Data = self.player_stats["atk"]

        return Player_Attack_Data

    def Enemy(self):
        if self.debug:
            print(f"{ANSI.NEW_LINE}{ANSI.BRIGHT_MAGENTA}{ANSI.SAPERATOR}{ANSI.RESET}")
            for key, value in self.enemy.items():
                print(f"{ANSI.YELLOW}{key}: {value}{ANSI.RESET}")
            ## id
            ## name
            ## lvl
            ## hp
            ## max_hp
            ## attack
            ## defense
            ## speed
            ## exp_drop
            ## rarity
            ## resistance
            ## attack_type
            ## boss
            print(f"{ANSI.NEW_LINE}{ANSI.BRIGHT_MAGENTA}{ANSI.SAPERATOR}{ANSI.RESET}")
        Enemy_Attack_Data = self.enemy["attack"]
        return Enemy_Attack_Data


    def Attack_Cycle(self, Player_Attack_Data, Enemy_Attack_Data):
        print(f"{ANSI.CYAN}{ANSI.BOLD} Player: {Player_Attack_Data} {ANSI.NEW_LINE} Enemy:{Enemy_Attack_Data}{ANSI.RESET}")