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

def send_message(self,message):
    try:
        self.sock.send(message.encode('ascii'))
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 65432
    request = {
        "content": "shaurya says geeksforgeeks",
        "type": "text",
        "encoding": "ascii"
    }

    try:
        start_client(host, port, request)
        while True:
            events = sel.select()
            for key, mask in events:
                message = key.data
                if mask & selectors.EVENT_WRITE:
                    # Send a message to the server here
                    message.sock.send(request["content"].encode('ascii'))
                elif mask & selectors.EVENT_READ:
                    process_response(message)

    except KeyboardInterrupt:
        print("Client application shutting down.")