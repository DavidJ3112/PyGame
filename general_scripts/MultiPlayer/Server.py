import threading
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("localhost", 5555))
server.listen()

clients = []

while True:
    client, addr = server.accept()
    print(f"Connected: {addr}")
    clients.append(client)

    client.send("welcome to the server".encode())