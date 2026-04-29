import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))

sys.path.append(parent_dir)

from general_scripts.ANSI import ANSI
import pygame

class Game:
    class PvE:
        def __init__(self):
            pass

        def Attack(self):
            print("Attack")

        def Guard(self):
            print("Guard")

        def Item(self):
            print("Item")

        def Flee(self):
            print("Flee")

if __name__ == "__main__":
    game = Game.PvE()
    game.Attack()
    game.Guard()
    game.Item()
    game.Flee()