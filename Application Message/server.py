import sys
import socket
import selectors
import libclient
import struct
import json
import base64
import os

HOST = "127.0.0.1"  # Use your localhost IP address
PORT = 65432  # Port should be an integer

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server is listening on {HOST}:{PORT}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)  # Receive up to 1024 bytes of data
                if not data:
                    break
                conn.sendall(data)
except socket.error as e:
    print(f"An error occurred: {e}")

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