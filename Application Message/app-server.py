import sys
import socket
import selectors
import struct
import json
from libserver import Message

sel = selectors.DefaultSelector()

def accept_connections(server_socket):
    conn, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    message = Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)

if __name__ == '__main__':
    host = "127.0.0.1"
    port = 65432

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    server.setblocking(False)

    sel.register(server, selectors.EVENT_READ, data=None)

    print(f"Server is running on {host}:{port}")

    try:
        while True:
            events = sel.select()
            for key, mask in events:
                if key.data is None:
                    accept_connections(key.fileobj)
                else:
                    message = key.data
                    try:
                        message.process_events(mask)
                    except Exception as e:
                        print(f"Error: Exception for {message.addr}: {e}")
                        message.close()
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        sel.close()
