"""
example_game.py  —  shows how to use network.py in a real game
Run the server in one terminal, then the client in another.
"""

from network import GameServer, GameClient
import threading
import time


#!^ ─────────────────────────────────────────────
#!^  GAME SERVER
#!^ ─────────────────────────────────────────────

class MyGameServer(GameServer):

    def On_Connect(self, gid):
        #!^ tell everyone a new player joined
        self.Broadcast({"type": "player_joined", "gid": gid})

    def On_Message(self, gid, conn, data):
        if data.get("type") == "input":
            x, y = data.get("x", 0), data.get("y", 0)
            print(f"  Player {gid} moved to ({x}, {y})")

            self.Broadcast(
                {"type": "player_moved", "gid": gid, "x": x, "y": y},
                exclude=conn
            )

    def On_Disconnect(self, gid):
        self.Broadcast({"type": "player_left", "gid": gid})


#!^ ─────────────────────────────────────────────
#!^  GAME CLIENT
#!^ ─────────────────────────────────────────────

class MyGameClient(GameClient):

    def On_Ready(self):
        print(f"Joined the game! My GID is {self.gid}")

    def On_Message(self, data):
        t = data.get("type")
        if t == "player_joined":
            print(f"  >> Player {data['gid']} joined the game")
        elif t == "player_moved":
            print(f"  >> Player {data['gid']} is at ({data['x']}, {data['y']})")
        elif t == "player_left":
            print(f"  >> Player {data['gid']} left the game")

    def On_Disconnect(self):
        print("Lost connection to server!")


#!^ ─────────────────────────────────────────────
#!^  ENTRY POINTS
#!^ ─────────────────────────────────────────────

def Run_Server():
    server = MyGameServer(ADDRESS)

    threading.Thread(target=server._Start_Discovery_Beacon, daemon=True).start()

    server.Start()

def Run_Client(server_ip, poort, client_id=1):
    address = (server_ip, poort)
    client = MyGameClient(address)
    client.Connect()

    if not client.Wait_Until_Ready():
        print(f"[Client {client_id}] Timed out!")
        return

    print(f"[Client {client_id}] Joined with GID: {client.gid}")

    try:
        # Move in a circle or pattern so you can see them all working
        for i in range(10):
            client.Send({
                "type": "input", 
                "x": i * 10 + (client_id * 5), 
                "y": i * 5
            })
            time.sleep(1)
    finally:
        client.Disconnect()
        print(f"[Client {client_id}] Disconnected.")

def Run_Multi_Clients(server_ip, poort, count=10):
    threads = []
    print(f"--- Spawning {count} Clients ---")
    
    for i in range(count):
        t = threading.Thread(target=Run_Client, args=(server_ip, poort, i+1))
        t.start()
        threads.append(t)
        time.sleep(0.1) 

    # Wait for all of them to finish
    for t in threads:
        t.join()

poort = 5000

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python example_game.py server | client")
    elif sys.argv[1] == "server":
        selected_ip = MyGameServer.Get_Address()
        ADDRESS = (selected_ip, poort)

        Run_Server()
    elif sys.argv[1] == "client":
        target = MyGameClient.Discover_Server()

        if not target:
            target = input("Could not find server. Enter IP manually [127.0.0.1]: ").strip()
            if not target:
                target = "127.0.0.1"

        Run_Client(target, poort=5000)
        # Run_Multi_Clients(target, poort, 1)