import socket

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
