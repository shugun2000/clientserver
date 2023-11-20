import sys
import socket
import selectors
import libclient
import struct
import json
import base64
import os

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

    upload_file(client_socket, "example.txt")

def handle_response(response):
    if response["type"] == "download":
        filename = response["filename"]
        content = base64.b64decode(response["content"])
        with open(filename, 'wb') as file:
            file.write(content)
        print(f"Downloaded file: {filename}")

def process_response(message):
    message.process_protoheader()
    if message._jsonheader_len is not None:
        message.process_jsonheader()
    if message.request:
        message.process_request()
    if message.response:
        print("Received a response:", message.response)
        handle_response(message.response)

        if message.events & selectors.EVENT_READ:
            response = message.response
            if response["type"] == "download":
                filename = response["filename"]
                content = base64.b64decode(response["content"])
                with open(filename, 'wb') as file:
                    file.write(content)
                print(f"Downloaded file: {filename}")

def send_message(self,message):
    try:
        self.sock.send(message.encode('ascii'))
    except Exception as e:
        print(f"Error sending message: {e}")

def upload_file(client_socket, filename):
    try:
        with open(filename, 'rb') as file:
            content = file.read()
            encoded_content = base64.b64encode(content).decode('ascii')
            request = {
                "type": "upload",
                "filename": os.path.basename(filename),
                "content": encoded_content,
            }
            request_json = json.dumps(request)
            client_socket.send(request_json.encode('ascii'))
        print(f"Uploaded file: {filename}")
    except Exception as e:
        print(f"Error uploading file: {e}")

def download_file(client_socket, filename):
    try:
        request = {
            "type": "download",
            "filename": filename,
        }
        request_json = json.dumps(request)
        client_socket.send(request_json.encode('ascii'))

        response = client_socket.recv(4096)  # Receive the response from the server
        response_data = json.loads(response.decode('ascii'))
        if response_data["type"] == "download":
            content = base64.b64decode(response_data["content"])
            with open(filename, 'wb') as file:
                file.write(content)
            print(f"Downloaded file: {filename}")
    except Exception as e:
        print(f"Error downloading file: {e}")

if mask & selectors.EVENT_READ:
    response = message.response
    if response["type"] == "download":
        filename = response["filename"]
        content = base64.b64decode(response["content"])
        with open(filename, 'wb') as file:
            file.write(content)
        print(f"Downloaded file: {filename}")

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
                    process_response(message, mask)

    except KeyboardInterrupt:
        print("Client application shutting down.")