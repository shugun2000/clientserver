import sys
import socket
import threading

from libserver import Message

def accept_connections(server_socket):
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_socket.setblocking(False)
        message = Message(client_socket, client_address)
        message.start()

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 65432
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)

print(f"Server is running on {host}:{port}")

try:
    while True:
        accept_connections(server_socket)
except KeyboardInterrupt:
        print("Server shutting down.")
finally:
        server_socket.close()