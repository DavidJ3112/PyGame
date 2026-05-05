import socket
import threading
import json
import time


#!^ ─────────────────────────────────────────────
#!^  BASE SERVER
#!^ ─────────────────────────────────────────────

class GameServer:
    """
    Reusable TCP game server base class.

    Usage:
        class MyServer(GameServer):
            def on_connect(self, gid):
                print(f"Player {gid} joined!")

            def on_message(self, gid, conn, data):
                #!^ handle incoming message, send replies with self.send(conn, {...})
                self.send(conn, {"type": "ack", "gid": gid})

            def on_disconnect(self, gid):
                print(f"Player {gid} left.")

        server = MyServer(("0.0.0.0", 5000))
        server.start()
    """

    def __init__(self, address):
        self.address = address
        self.next_gid = 1
        self.clients = {}   #!^ conn -> gid
        self._lock = threading.Lock()

    #!^ ── override these in your game ──────────────────

    def on_connect(self, gid):
        """Called when a new client connects."""
        pass

    def on_message(self, gid, conn, data):
        """Called for every JSON message received from a client."""
        pass

    def on_disconnect(self, gid):
        """Called when a client disconnects."""
        pass

    #!^ ── helpers ──────────────────────────────────────

    def send(self, conn, data):
        """Send a JSON message to one client."""
        try:
            conn.sendall((json.dumps(data) + "\n").encode())
        except OSError:
            pass

    def broadcast(self, data, exclude=None):
        """Send a JSON message to all connected clients."""
        with self._lock:
            targets = list(self.clients.items())
        for conn, gid in targets:
            if conn is not exclude:
                self.send(conn, data)

    def get_gid(self, conn):
        return self.clients.get(conn)

    def get_conn(self, gid):
        with self._lock:
            for conn, g in self.clients.items():
                if g == gid:
                    return conn
        return None

    #!^ ── internals ────────────────────────────────────

    def _handle_client(self, conn, addr):
        conn.settimeout(60.0)
        gid = self.clients[conn]
        print(f"[server] GID {gid} connected: {addr}")

        self.send(conn, {"type": "welcome", "gid": gid})
        self.on_connect(gid)

        buffer = ""
        try:
            while True:
                try:
                    part = conn.recv(1024)
                except ConnectionResetError:
                    break  #!^ Windows throws this instead of returning b"" on disconnect
                if not part:
                    break

                buffer += part.decode()

                while "\n" in buffer:
                    msg, buffer = buffer.split("\n", 1)
                    if not msg.strip():
                        continue

                    try:
                        data = json.loads(msg)
                    except json.JSONDecodeError:
                        continue

                    self.on_message(gid, conn, data)

        finally:
            conn.close()
            with self._lock:
                self.clients.pop(conn, None)
            self.on_disconnect(gid)
            print(f"[server] GID {gid} disconnected")

    def start(self):
        """Start the server (blocking — runs until Ctrl+C)."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(self.address)
        server.listen()
        server.settimeout(1.0)
        print(f"[server] Listening on {self.address}")

        try:
            while True:
                try:
                    conn, addr = server.accept()
                except socket.timeout:
                    continue

                with self._lock:
                    gid = self.next_gid
                    self.next_gid += 1
                    self.clients[conn] = gid

                threading.Thread(
                    target=self._handle_client,
                    args=(conn, addr),
                    daemon=True
                ).start()

        except KeyboardInterrupt:
            print("[server] Shutting down...")
        finally:
            server.close()
            print("[server] Stopped.")


#!^ ─────────────────────────────────────────────
#!^  BASE CLIENT
#!^ ─────────────────────────────────────────────

class GameClient:
    """
    Reusable TCP game client base class.

    Usage:
        class MyClient(GameClient):
            def on_ready(self):
                print("Connected! My GID:", self.gid)

            def on_message(self, data):
                print("Server says:", data)

        client = MyClient(("10.19.12.127", 5000))
        client.connect()
        #!^ do stuff...
        client.send({"type": "input", "x": 10, "y": 5})
    """

    def __init__(self, address):
        self.address = address
        self.gid = None
        self._conn = None
        self._buffer = ""

    #!^ ── override these in your game ──────────────────

    def on_ready(self):
        """Called once the welcome message is received and gid is set."""
        pass

    def on_message(self, data):
        """Called for every JSON message from the server (after welcome)."""
        pass

    def on_disconnect(self):
        """Called when the connection drops."""
        pass

    #!^ ── helpers ──────────────────────────────────────

    def send(self, data):
        """Send a JSON message to the server."""
        if self._conn:
            try:
                self._conn.sendall((json.dumps(data) + "\n").encode())
            except OSError:
                pass

    def wait_until_ready(self, timeout=10.0):
        """Block until gid is assigned (welcome received) or timeout."""
        deadline = time.time() + timeout
        while self.gid is None and time.time() < deadline:
            time.sleep(0.05)
        return self.gid is not None

    #!^ ── internals ────────────────────────────────────

    def _receive_loop(self):
        if self._conn is None:
            return
        while True:
            try:
                part = self._conn.recv(1024)
            except OSError:
                break

            if not part:
                break

            self._buffer += part.decode()

            while "\n" in self._buffer:
                msg, self._buffer = self._buffer.split("\n", 1)
                if not msg.strip():
                    continue

                try:
                    data = json.loads(msg)
                except json.JSONDecodeError:
                    continue

                if data.get("type") == "welcome":
                    self.gid = data["gid"]
                    print(f"[client] Connected — GID: {self.gid}")
                    self.on_ready()
                else:
                    self.on_message(data)

        self.on_disconnect()
        print("[client] Disconnected.")

    def connect(self, start_loop=True):
        """Connect to the server and start the receive loop in a thread."""
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._conn.connect(self.address)
        print(f"[client] Connected to {self.address}")

        if start_loop:
            threading.Thread(target=self._receive_loop, daemon=True).start()

    def disconnect(self):
        if self._conn:
            self._conn.close()