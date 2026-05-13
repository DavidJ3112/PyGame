import os
import sys
import threading
import pygame
import socket
import time
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

from general_scripts.network import GameServer, GameClient
from general_scripts.Helpers import console

console.set_max_logs(count=25)


class MyServer(GameServer):
    def __init__(self, address, game_id, version, game_logic=None):
        super().__init__(address, game_id, version)
        self.player_symbols = {}
        self.next_symbol = "x"
        self.game_instance = game_logic

    def On_Connect(self, gid):
        console.log("SUCCESS", f"Player GID {gid} connected.")

        symbol = self.next_symbol
        self.player_symbols[gid] = symbol
        self.next_symbol = "o" if self.next_symbol == "x" else "x"

        conn = self.Get_Conn(gid)

        self.Send(conn, {"type": "assignment", "symbol": symbol})

        self.Broadcast({"type": "player_joined", "gid": gid}, exclude=conn)

    def On_Message(self, gid, conn, data):
        if data.get("type") == "player_move":
            ## console.log("INFO", f"{gid = }  {data = }")
            assert self.game_instance is not None
            result, winner = self.game_instance.process_move(gid, data)
            if result == True:
                self.Broadcast(
                    {"type": "MSG", "MSG": f"Player {gid}, made vaild move {result}"}
                )
            elif result == {"type":"MSG","MSG":"No Vaild Moves Posible"}:
                self.Broadcast({"type":"MSG","MSG":"No Vaild Moves Posible"})
            if winner:
                self.Broadcast({"type": "Win", "Winner": winner})

    def On_Disconnect(self, gid):
        console.log("WARN", f"Player GID {gid} disconnected.")

        if gid in self.player_symbols:
            del self.player_symbols[gid]

        self.Broadcast({"type": "player_left", "gid": gid})


class MyClient(GameClient):
    def __init__(self, address, game_id, version):
        super().__init__(address, game_id, version)
        self.game_ref = None
        self.is_reconnecting = False

    def Connect(self, start_loop=True):
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._conn.settimeout(5.0)
        try:
            self._conn.connect(self.address)

            handshake = {"type": "handshake", "session_id": self.session_id}
            self.Send(handshake)

            if start_loop:
                threading.Thread(target=self._Receive_Loop, daemon=True).start()
                threading.Thread(target=self._Heartbeat_Loop, daemon=True).start()
        except Exception as e:
            raise e

    def On_Ready(self):
        console.log("SUCCESS", f"Joined the game! My GID is {self.gid}")
        self.is_reconnecting = False

    def On_Message(self, data):
        if data.get("type") == "assignment":
            self.symbol = data["symbol"]
            console.log("INFO", f"Assigned symbol: {self.symbol}")
            return

        if data.get("type") == "MSG":
            console.log("INFO", data["MSG"])

        if data.get("type") == "Win":
            console.log("INFO", data["Winner"])

        if data.get("type") == "board_update":
            if self.game_ref:
                self.game_ref.current_board = data["board"]

    def _Receive_Loop(self):
        if self._conn is None:
            return
        try:
            while True:
                part = self._conn.recv(1024)
                if not part:
                    break

                self._buffer += part.decode()
                while "\n" in self._buffer:
                    msg, self._buffer = self._buffer.split("\n", 1)
                    if not msg.strip():
                        continue
                    try:
                        data = json.loads(msg)

                        if data.get("type") == "error":
                            console.log("ERROR", f"REJECTED: {data.get('message')}")
                            self.gid = "REJECTED"
                            return

                        if data.get("type") == "welcome":
                            self.gid = data["gid"]
                            self.session_id = data.get("session_id")
                            if "symbol" in data:
                                self.symbol = data["symbol"]
                            self.On_Ready()
                        else:
                            self.On_Message(data)
                    except json.JSONDecodeError:
                        continue
        except Exception:
            pass
        finally:
            if self.gid != "REJECTED":
                self.On_Disconnect()

    def On_Disconnect(self):
        if self.gid == "REJECTED":
            return

        if self.is_reconnecting:
            return
        self.is_reconnecting = True

        console.log("ERROR", "Lost connection! Attempting to reconnect...")

        attempts = 0
        max_attempts = 10

        while attempts < max_attempts:
            try:
                console.log("INFO", f"Reconnect attempt {attempts + 1}...")

                self.gid = None
                self.Connect()

                self.Wait_Until_Ready(timeout=3.0)

                if self.gid == "REJECTED":
                    console.log("WARN", "Server is full. Aborting reconnection.")
                    break  # Kill the loop

                if self.gid is not None:
                    console.log(
                        "SUCCESS", f"Re-established connection! GID: {self.gid}"
                    )
                    self.is_reconnecting = False
                    return

            except Exception as e:
                console.log("WARN", f"Attempt {attempts + 1} failed: {e}")

            attempts += 1
            time.sleep(2)

        console.log("ERROR", "Recovery failed. Exiting.")
        if self.game_ref:
            self.game_ref.running = False


#!# --- Game Loops ---


class ServerGame:
    def __init__(self, server_instance) -> None:
        self.Clock = pygame.time.Clock()
        self.server = server_instance
        self.running = True
        self.board = []
        self.turn = "x"
        self.FPS = 24

        self.board_size = 3
        self.win_length = 3

    def construct_board(self):
        game_board_sizes = (self.board_size, self.board_size)
        self.board = []
        for _ in range(game_board_sizes[0]):
            current_row = []
            for _ in range(game_board_sizes[1]):
                current_row.append("")
            self.board.append(current_row)
        return self.board

    def Loop(self):
        console.log("INFO", "Game Logic Loop Started.")
        self.construct_board()

        while self.running:
            self.Clock.tick(self.FPS)

            self.server.Broadcast({"type": "board_update", "board": self.board})

            time.sleep(0.2)

    def check_winstate(self, row, col, symbol, k=3):
        board = self.board
        n = len(board)

        directions = [
            (0, 1),  # horizontal
            (1, 0),  # vertical
            (1, 1),  # diagonal down-right
            (1, -1),  # diagonal down-left
        ]

        for dr, dc in directions:
            count = 1

            # forward direction
            r, c = row + dr, col + dc
            while 0 <= r < n and 0 <= c < n and board[r][c] == symbol:
                count += 1
                r += dr
                c += dc

            # backward direction
            r, c = row - dr, col - dc
            while 0 <= r < n and 0 <= c < n and board[r][c] == symbol:
                count += 1
                r -= dr
                c -= dc

            if count >= k:
                return True

        return False

    def process_move(self, gid, data):
        row = data["click_row"]
        col = data["click_col"]
        symbol = data["symbol"]

        if any("" in row for row in self.board):
            if self.turn == symbol:
                if self.board[row][col] == "":
                    self.board[row][col] = symbol
                    if symbol == "x":
                        self.turn = "o"
                    if symbol == "o":
                        self.turn = "x"

                    console.log("SUCCESS", f"Move accepted: {symbol} at ({row}, {col})")
                    if self.check_winstate(row, col, symbol, self.win_length):
                        console.log("INFO", f"{symbol} wins the game!")
                        self.construct_board()
                        msg = f"{symbol} wins the game!"
                        return ({row}, {col}), msg

                    return ({row}, {col}), None

            console.log("WARN", f"Invalid move attempted by {gid}")
        else:
            console.log("INFO","No Vaild moves posible, reseting the board")
            self.construct_board()
            return ({"type":"MSG","MSG":"No Vaild Moves Posible"}), False

        console.log("WARN", f"Early move attempted by {gid}")
        return False, None


class PlayerGame:
    def __init__(self, client_instance) -> None:
        pygame.init()
        self.running = True
        self.client = client_instance
        self.client.game_ref = self
        self.current_board = None

        self.screen = pygame.display.set_mode((640, 640))
        self.Clock = pygame.time.Clock()
        self.BGC = (25, 25, 25)
        self.FPS = 24
        self.board_update = False

        self.current_board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
        ]

    def Loop(self):
        while self.running:
            pygame.display.set_caption(f"Tic Tac Toe Player: {self.client.symbol}")
            self.Clock.tick(self.FPS)

            self.screen.fill(self.BGC)
            self.Events()
            if self.current_board:
                self.Draw_Board(self.current_board)
        pygame.quit()

    def Events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.client.Disconnect("User closed game")
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    console.log("WARN", "SIMULATING CRASH: Dropping socket...")
                    self.client._conn.close()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.current_board and hasattr(self.client, "symbol"):
                        rows, cols = len(self.current_board), len(self.current_board[0])
                        w, h = self.screen.get_size()
                        cw, ch = w // cols, h // rows

                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        self.col = mouse_x // cw
                        self.row = mouse_y // ch

                    self.client.Send(
                        {
                            "type": "player_move",
                            "GID": self.client.gid,
                            "symbol": self.client.symbol,
                            "click_col": self.col,
                            "click_row": self.row,
                        }
                    )

    def Draw_Board(self, board):
        if self.client.is_reconnecting:
            font = pygame.font.SysFont("Arial", 30)
            text = font.render("RECONNECTING...", True, (255, 255, 0))
            self.screen.blit(text, (20, 20))

        rows, cols = len(board), len(board[0])
        w, h = self.screen.get_size()
        cw, ch = w // cols, h // rows

        for r in range(rows):
            for c in range(cols):
                rect = pygame.Rect(c * cw, r * ch, cw, ch)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
                val = board[r][c]
                center = (c * cw + cw // 2, r * ch + ch // 2)
                if val == "x":
                    pad = cw // 4
                    pygame.draw.line(
                        self.screen,
                        (255, 0, 0),
                        (c * cw + pad, r * ch + pad),
                        (c * cw + cw - pad, r * ch + ch - pad),
                        3,
                    )
                    pygame.draw.line(
                        self.screen,
                        (255, 0, 0),
                        (c * cw + cw - pad, r * ch + pad),
                        (c * cw + pad, r * ch + ch - pad),
                        3,
                    )
                elif val == "o":
                    pygame.draw.circle(self.screen, (0, 0, 255), center, cw // 3, 3)
        pygame.display.flip()


#!# --- Execution ---


def Run_Server(ip, port):
    addr = (ip, port)
    server = MyServer(addr, game_id="DR_TicTacToe", version="2.0")
    game = ServerGame(server)

    server.game_instance = game

    console.log("INFO", f"Starting server discovery beacon...")
    threading.Thread(target=server._Start_Discovery_Beacon, daemon=True).start()
    threading.Thread(
        target=server.Start, kwargs={"max_players": 2}, daemon=True
    ).start()

    game.Loop()


def Run_Client(ip, port):
    addr = (ip, port)
    client = MyClient(addr, game_id="DR_TicTacToe", version="2.0")
    console.log("INFO", f"Connecting to {ip}:{port}...")
    try:
        client.Connect()
    except Exception as e:
        console.log("ERROR", f"Initial connection failed: {e}")
        return

    client.Wait_Until_Ready(timeout=3.0)

    #!^ Check the GID immediately after waiting
    if client.gid == "REJECTED":
        console.log("ERROR", "Connection failed: Server is full.")
        return

    if client.gid is None:
        console.log("ERROR", "Handshake timeout.")
        return

    game = PlayerGame(client)
    game.Loop()
    client.Disconnect()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python example_game.py server | client")
    elif sys.argv[1] == "server":
        ip = MyServer.Get_Address()
        p_raw = console.ask("Enter Port [Default 5000]")
        port = int(p_raw) if p_raw.isdigit() else 5000
        console.log("INFO", f"Server running at {ip}:{port}")
        Run_Server(ip, port)
    elif sys.argv[1] == "client":
        ip = MyClient.Discover_Server()
        if not ip:
            ip = console.ask("Server not found. Enter IP [127.0.0.1]") or "127.0.0.1"
        p_raw = console.ask("Enter Port [Default 5000]")
        port = int(p_raw) if p_raw.isdigit() else 5000
        Run_Client(ip, port)
