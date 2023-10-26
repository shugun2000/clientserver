import sys
import socket
import selectors
import types
import traceback 
import threading

from libserver import Message

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    message = Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)

sel = selectors.DefaultSelector()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 65432))
server.listen(10)

def start_server():
    try:
        while True:
            events = sel.select(timeout=1)
            print(f"Selected events: {events}")
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    message = key.data
                    try:
                        message.process_events(mask)
                    except Exception:
                        print(
                            f"Main: Error: Exception for {message.addr}:\n"
                            f"{traceback.format_exc()}"
                        )

    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        sel.close()

start_server()
