try:
    from ANSI import ANSI
    from Helpers import console
except ImportError:
    from .ANSI import ANSI
    from .Helpers import console

import threading
import socket
import json
import uuid
import time

#!^ ─────────────────────────────────────────────
#!^  BASE SERVER
#!^ ─────────────────────────────────────────────

class GameServer:
    """Base class for a threaded TCP game server with session management."""
    
    def __init__(self, address, game_id=None, version=None, heartbeat_timeout=30):
        """
        Initialize the server settings and session tracking.
        Args:
            address (tuple): (ip, port) to bind the server.
            game_id (str): Optional identifier for branding/validation.
            version (str): Optional version string for compatibility checks.
            heartbeat_timeout (int): Seconds before a silent client is kicked.
        """
        self.address = address
        self.game_id = game_id
        self.version = version
        
        self.next_gid = 1
        self.clients = {}   #!^ conn -> gid
        self.sessions = {}  #!^ conn -> uuid_str
        self._lock = threading.Lock()
        
        #!^ Heartbeat & Session Tracking
        self.last_seen = {}        #!^ conn -> timestamp
        self.heartbeat_timeout = heartbeat_timeout 
        self.reconnect_map = {}    #!^ uuid -> {"gid": int, "expiry": float}
        self.session_timeout = 300 #!^ 5 minute window to rejoin

        threading.Thread(target=self._Heartbeat_Reaper, daemon=True).start()

    #!^ --- Overrides ---
    def On_Connect(self, gid): 
        """Callback triggered when a client successfully connects."""
        pass

    def On_Message(self, gid, conn, data): 
        """Callback triggered when a valid JSON message is received."""
        pass

    def On_Disconnect(self, gid): 
        """Callback triggered when a client disconnects or times out."""
        pass

    #!^ --- Heartbeat Reaper ---
    def _Heartbeat_Reaper(self):
        """Internal loop to disconnect clients exceeding the heartbeat_timeout."""
        while True:
            time.sleep(5)
            now = time.time()
            to_kick = []
            
            with self._lock:
                for conn, last_time in self.last_seen.items():
                    if now - last_time > self.heartbeat_timeout:
                        to_kick.append(conn)
            
            for conn in to_kick:
                gid = self.Get_Gid(conn)
                console.log("WARN", f"GID {gid} timed out (Heartbeat missed)")
                try:
                    conn.close()
                except:
                    pass

    #!^ --- Branding Logic ---
    def _Validate_Brand(self, data):
        """
        Verifies that incoming data matches server game_id and version.
        Args:
            data (dict): The message payload to validate.
        Returns:
            tuple: (bool success, str error_message)
        """
        if self.game_id and data.get("game_id") != self.game_id:
            return False, f"Game ID Mismatch (Expected {self.game_id})"
        if self.version and data.get("version") != self.version:
            return False, f"Version Mismatch (Expected {self.version})"
        return True, ""

    #!^ --- Helpers ---
    @staticmethod
    def Get_Address():
        """Prompts the user to select an available local IP address."""
        host_name = socket.gethostname()
        addr_info = socket.getaddrinfo(host_name, None, socket.AF_INET, socket.SOCK_STREAM)
        ips = list(set([info[4][0] for info in addr_info]))
        if "127.0.0.1" not in ips: ips.append("127.0.0.1")

        console.log("NOTICE", "--- Available Network Interfaces ---", False, False)
        for i, ip in enumerate(ips):
            console.log("NOTICE", f"{i + 1}. {ip}", False, False)

        while True:
            selection = console.ask(f"Select IP (1-{len(ips)}) [Default 1]").strip()
            if not selection: return ips[0]
            try:
                index = int(selection) - 1
                if 0 <= index < len(ips): return ips[index]
            except ValueError: pass
            console.log("ERROR", "Invalid selection. Please try again.")

    def Send(self, conn, data):
        """
        Sends a JSON-encoded message to a specific connection.
        Args:
            conn (socket): The recipient's socket object.
            data (dict): The dictionary payload to send.
        """
        if self.game_id: data["game_id"] = self.game_id
        if self.version: data["version"] = self.version
        try:
            conn.sendall((json.dumps(data) + "\n").encode())
        except (OSError, BrokenPipeError): pass

    def Broadcast(self, data, exclude=None):
        """
        Sends a message to all connected clients.
        Args:
            data (dict): The dictionary payload to send.
            exclude (socket): Optional socket to skip during broadcast.
        """
        with self._lock:
            targets = list(self.clients.items())
        for conn, gid in targets:
            if conn is not exclude:
                self.Send(conn, data)

    def Get_Gid(self, conn):
        """Returns the Game ID (gid) associated with a socket."""
        with self._lock:
            return self.clients.get(conn)

    def Get_Conn(self, gid):
        """Returns the socket object associated with a Game ID (gid)."""
        with self._lock:
            for conn, g in self.clients.items():
                if g == gid: return conn
        return None

    #!^ --- Discovery ---
    def _Start_Discovery_Beacon(self, port=6000):
        """
        Starts a UDP broadcast loop to let clients find the server.
        Args:
            port (int): UDP port to broadcast on.
        """
        broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        beacon_data = {
            "type": "server_discovery", 
            "port": self.address[1],
            "game_id": self.game_id
        }
        message = json.dumps(beacon_data).encode()
        console.log("INFO", f"Discovery beacon active (Brand: {self.game_id or 'None'})")
        
        while True:
            try:
                broadcast_sock.sendto(message, ("<broadcast>", port))
                time.sleep(2)
            except Exception: break

    #!^ --- Client Handling ---
    def _Handle_Client(self, conn, addr):
        """
        Internal loop for managing a single client connection.
        Args:
            conn (socket): The client socket.
            addr (tuple): The client (ip, port).
        """
        conn.settimeout(45.0) 
        gid = None
        client_uuid = None

        try:
            raw = conn.recv(1024).decode().strip()
            if not raw: return
            
            try:
                handshake = json.loads(raw)
                client_uuid = handshake.get("session_id")
                valid, error_msg = self._Validate_Brand(handshake)
                if not valid:
                    console.log("WARN", f"Rejected {addr}: {error_msg}")
                    self.Send(conn, {"type": "error", "message": error_msg})
                    return
            except json.JSONDecodeError: return

            with self._lock:
                now = time.time()
                if client_uuid and client_uuid in self.reconnect_map and now < self.reconnect_map[client_uuid]["expiry"]:
                    session_info = self.reconnect_map.pop(client_uuid)
                    gid = session_info["gid"]
                else:
                    gid = self.next_gid
                    self.next_gid += 1
                    if not client_uuid: client_uuid = str(uuid.uuid4())

                self.clients[conn] = gid
                self.sessions[conn] = client_uuid
                self.last_seen[conn] = time.time() 

            console.log("INFO", f"GID {gid} connected from {addr}")
            self.Send(conn, {"type": "welcome", "gid": gid, "session_id": client_uuid})
            self.On_Connect(gid)

            buffer = ""
            while True:
                try:
                    part = conn.recv(1024)
                except (socket.timeout, TimeoutError, ConnectionResetError): break
                if not part: break

                buffer += part.decode()
                while "\n" in buffer:
                    msg, buffer = buffer.split("\n", 1)
                    if not msg.strip(): continue
                    try:
                        data = json.loads(msg)
                        
                        with self._lock:
                            self.last_seen[conn] = time.time()

                        if data.get("type") == "heartbeat": 
                            continue 
                        
                        valid, _ = self._Validate_Brand(data)
                        if valid:
                            self.On_Message(gid, conn, data)
                    except json.JSONDecodeError: continue
        finally:
            with self._lock:
                if conn in self.clients:
                    this_gid = self.clients.pop(conn)
                    this_uid = self.sessions.pop(conn)
                    self.last_seen.pop(conn, None)
                    self.reconnect_map[this_uid] = {
                        "gid": this_gid,
                        "expiry": time.time() + self.session_timeout
                    }
            conn.close()
            self.On_Disconnect(gid)

    def Start(self, max_players=0):
        """
        Binds the socket and begins accepting client connections.
        Args:
            max_players (int): Maximum concurrent connections (0 for unlimited).
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(self.address)
        server.listen()
        server.settimeout(1.0)
        
        console.header(f"Server Listening on {self.address}")

        try:
            while True:
                try:
                    conn, addr = server.accept()
                except socket.timeout: continue

                with self._lock:
                    if max_players != 0 and len(self.clients) >= max_players:
                        console.log("WARN", f"Connection rejected from {addr}: Server Full")
                        rejection = {"type": "error", "message": "Server is full!"}
                        try: conn.sendall((json.dumps(rejection) + "\n").encode())
                        except: pass
                        conn.close()
                        continue

                threading.Thread(target=self._Handle_Client, args=(conn, addr), daemon=True).start()
        except KeyboardInterrupt: pass
        finally: server.close()

#!^ ─────────────────────────────────────────────
#!^  BASE CLIENT
#!^ ─────────────────────────────────────────────

class GameClient:
    """Base class for a TCP game client with automatic heartbeat and discovery."""
    
    def __init__(self, address, game_id=None, version=None, bps=10):
        """
        Initialize client settings.
        Args:
            address (tuple): (ip, port) of the server.
            game_id (str): Optional identifier for validation.
            version (str): Optional version string for validation.
            bps (int): Beats Per Second (interval) for heartbeats.
        """
        self.address = address
        self.game_id = game_id
        self.version = version
        
        self.gid = None
        self.session_id = None 
        self._conn = None
        self._buffer = ""
        self.heartbeat_interval = bps

    def On_Ready(self): 
        """Callback triggered when the server sends the welcome handshake."""
        pass

    def On_Message(self, data): 
        """Callback triggered when a valid JSON message is received."""
        pass

    def On_Disconnect(self): 
        """Callback triggered when the connection is lost."""
        pass

    def _Heartbeat_Loop(self):
        """Internal loop to keep the connection alive via heartbeat messages."""
        while self._conn:
            try:
                self.Send({"type": "heartbeat"})
                time.sleep(self.heartbeat_interval)
            except:
                break

    @staticmethod
    def Discover_Server(port=6000, timeout=5.0):
        """
        Listens for a UDP server discovery beacon.
        Args:
            port (int): UDP port to listen on.
            timeout (float): Seconds to wait before giving up.
        Returns:
            str: The IP of the discovered server, or None.
        """
        listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("", port))
        listener.settimeout(timeout)
        try:
            data, addr = listener.recvfrom(1024)
            info = json.loads(data.decode())
            if info.get("type") == "server_discovery": return addr[0]
        except Exception: return None
        finally: listener.close()

    def Send(self, data):
        """
        Sends a JSON-encoded message to the server.
        Args:
            data (dict): The dictionary payload to send.
        """
        if self.game_id: data["game_id"] = self.game_id
        if self.version: data["version"] = self.version
        if self._conn:
            try: 
                self._conn.sendall((json.dumps(data) + "\n").encode())
            except OSError: 
                pass

    def Wait_Until_Ready(self, timeout=10.0):
        """
        Blocks until the client has connected and received a GID.
        Args:
            timeout (float): Max seconds to wait.
        Returns:
            bool: True if ready, False if timeout reached.
        """
        deadline = time.time() + timeout
        while self.gid is None and time.time() < deadline:
            time.sleep(0.05)
        return self.gid is not None

    def _Receive_Loop(self):
        """Internal loop for receiving and parsing messages from the server."""
        if self._conn is None: return
        while True:
            try:
                part = self._conn.recv(1024)
                if not part: break
                self._buffer += part.decode()
                while "\n" in self._buffer:
                    msg, self._buffer = self._buffer.split("\n", 1)
                    if not msg.strip(): continue
                    try:
                        data = json.loads(msg)
                        if self.game_id and data.get("game_id") != self.game_id:
                            continue

                        if data.get("type") == "welcome":
                            self.gid = data["gid"]
                            self.session_id = data.get("session_id")
                            self.On_Ready()
                        else: self.On_Message(data)
                    except json.JSONDecodeError: continue
            except Exception: break
        self.On_Disconnect()

    def Connect(self, start_loop=True):
        """
        Establishes a connection to the server and starts listener threads.
        Args:
            start_loop (bool): Whether to start receiving and heartbeat threads immediately.
        """
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._conn.connect(self.address)
            self.Send({"type": "handshake", "session_id": self.session_id}) 
            
            if start_loop:
                threading.Thread(target=self._Receive_Loop, daemon=True).start()
                threading.Thread(target=self._Heartbeat_Loop, daemon=True).start()
        except Exception as e:
            console.log("ERROR", f"Socket connection failed: {e}")
            raise e

    def Disconnect(self):
        """Closes the active socket connection."""
        if self._conn: 
            self._conn.close()
            self._conn = None