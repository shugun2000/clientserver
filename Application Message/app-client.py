import sys
import socket
import selectors
import libclient
import struct

sel = selectors.DefaultSelector()

def start_client(host, port, request):
    addr = (host, port)
    print(f"Starting connection to {addr}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    message = libclient.Message(sel, sock, addr, request)
    sel.register(sock, selectors.EVENT_WRITE, data=message)

def process_response(message):
    message.process_protoheader()
    if message._jsonheader_len is not None:
        message.process_jsonheader()
    if message.request:
        message.process_request()

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 65432
    request = b"binary test"

    try:
        start_client(host, port, request)
        while True:
            events = sel.select()
            for key, mask in events:
                message = key.data
                process_response(message)
    except KeyboardInterrupt:
        print("Client application shutting down.")
