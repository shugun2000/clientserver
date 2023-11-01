import sys
import socket
import threading
import libclient

def start_connection(host, port, request):
    addr = (host, port)
    print(f"Starting connection to {addr}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    message = libclient.Message(sock, addr, request)
    message.start()  
    
if __name__ == '__main__':
    host = '127.0.0.1'
    port = 65432
    request = b"binary test"

    try:
        while True:
            start_connection(host, port, request)
    except KeyboardInterrupt:
        print("Client application shutting down.")