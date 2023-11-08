import socket
import sys
import selectors
import libclient
import struct
import json
import base64
import os

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Wassup homie")
    data = s.recv(1024)

print(f"Received {data!r}")

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