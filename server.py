import socket
import threading

HEADER = 64 # This is 64 bytes that server can handle
PORT = 8080 #THERE ARE 10000 PORT ABOVE 1000 is goo for you 
SERVER = "192.168.65.1" # CHANGE THIS WHENEVER YOU ARE IN DIFFERENT NETWORK
SERVER = socket.gethostbyname(socket.gethostname()) #THIS IS THE SAME ABOVE BUT BETTER, YOU DON'T NEED TO CHANGE, CAN DELETE LINE ABOVE
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

#from this  make a socket to allow open device to other connections

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #in bracket is your socket family name, sock stream is type
server.bind(ADDR)

def handle_client(conn, addr): # handle between client and server communication
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # this is how many bytes you want to receive from client in bracket
        msg_length = int(msg_length).decode(FORMAT)
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            connected = False

        print(f"[{addr}] {msg}") # This help receive the message from what client say
    
    conn.close()


def start(): # handle connection and distribute where they need to go
    server.listen()
    print(f"[LISTENING] Server is connected to your IP {SERVER}")
    while True: #this makes a loop for server to keep running. conn = connection, addr = address
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}")

print("[STARTING] server is starting...")
start()