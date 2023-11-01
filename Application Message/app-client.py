import sys
import socket
import selectors
import libclient
import struct

sel = selectors.DefaultSelector()

def connect_to_server(host, port):
    addr = (host, port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setblocking(False)
    client_socket.connect_ex(addr)
    return client_socket

def start_client(host, port, request):
    client_socket = connect_to_server(host, port)
    addr = (host, port)
    print(f"Starting connection to {addr}")
    message = libclient.Message(client_socket, addr, request=None)
    sel.register(client_socket, selectors.EVENT_WRITE, data=message)

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
