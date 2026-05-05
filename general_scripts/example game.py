"""
example_game.py  —  shows how to use network.py in a real game
Run the server in one terminal, then the client in another.
"""

import time
from network import GameServer, GameClient


#!^ ─────────────────────────────────────────────
#!^  GAME SERVER
#!^ ─────────────────────────────────────────────

class MyGameServer(GameServer):

    def on_connect(self, gid):
        #!^ tell everyone a new player joined
        self.broadcast({"type": "player_joined", "gid": gid})

    def on_message(self, gid, conn, data):
        if data.get("type") == "input":
            x, y = data.get("x", 0), data.get("y", 0)
            print(f"  Player {gid} moved to ({x}, {y})")

            self.broadcast(
                {"type": "player_moved", "gid": gid, "x": x, "y": y},
                exclude=conn
            )

    def on_disconnect(self, gid):
        self.broadcast({"type": "player_left", "gid": gid})


#!^ ─────────────────────────────────────────────
#!^  GAME CLIENT
#!^ ─────────────────────────────────────────────

class MyGameClient(GameClient):

    def on_ready(self):
        print(f"Joined the game! My GID is {self.gid}")

    def on_message(self, data):
        t = data.get("type")
        if t == "player_joined":
            print(f"  >> Player {data['gid']} joined the game")
        elif t == "player_moved":
            print(f"  >> Player {data['gid']} is at ({data['x']}, {data['y']})")
        elif t == "player_left":
            print(f"  >> Player {data['gid']} left the game")

    def on_disconnect(self):
        print("Lost connection to server!")


#!^ ─────────────────────────────────────────────
#!^  ENTRY POINTS
#!^ ─────────────────────────────────────────────

ADDRESS = ("127.0.0.1", 5000)

def run_server():
    server = MyGameServer(ADDRESS)
    server.start()

def run_client():
    client = MyGameClient(ADDRESS)
    client.connect()

    if not client.wait_until_ready():
        print("Timed out waiting for server!")
        return

    #!^ send some position updates
    for i in range(5):
        client.send({"type": "input", "gid": client.gid, "x": i * 10, "y": i * 5})
        time.sleep(2)

    client.disconnect()


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python example_game.py server | client")
    elif sys.argv[1] == "server":
        run_server()
    elif sys.argv[1] == "client":
        run_client()