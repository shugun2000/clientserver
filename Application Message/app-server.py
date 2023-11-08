import sys
import socket
import selectors
import struct
import json
from libserver import Message
import base64
import os

sel = selectors.DefaultSelector()

def accept_connections(server_socket):
    conn, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    message = Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)

def process_request(self):
    if self.request:
        if self.request["type"] == "upload":
            self.handle_upload_request()
        elif self.request["type"] == "download":
            self.handle_download_request()

def handle_upload_request(self):
    try:
        filename = self.request["filename"]
        encoded_content = self.request["content"]
        content = base64.b64decode(encoded_content.encode('ascii'))
        with open(filename, 'wb') as file:
            file.write(content)
        print(f"Received and saved uploaded file: {filename}")
    except Exception as e:
        print(f"Error handling upload request: {e}")

def handle_download_request(self):
    try:
        filename = self.request["filename"]
        with open(filename, 'rb') as file:
            content = file.read()
            encoded_content = base64.b64encode(content).decode('ascii')
            response = {
                "type": "download",
                "filename": filename,
                "content": encoded_content,
            }
            self.send_response(response)
        print(f"Sent requested file: {filename}")
    except Exception as e:
        print(f"Error handling download request: {e}")

def process_events(self, mask):
    if mask & selectors.EVENT_READ:
        self.read()
        self.process_protoheader()
        if self._jsonheader_len is not None:
            self.process_jsonheader()
        if self.request:
            self.process_request()
    if mask & selectors.EVENT_WRITE:
        self.write()

def process_response(self):
    self.close()
    if self.response:
        if self.response["type"] == "download":
            filename = self.response["filename"]
            content = base64.b64decode(self.response["content"])
            with open(filename, 'wb') as file:
                file.write(content)
            print(f"Downloaded file: {filename}")


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
