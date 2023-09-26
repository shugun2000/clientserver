import socket

HEADER = 64 # This is 64 bytes that server can handle
PORT = 8080 #THERE ARE 10000 PORT ABOVE 1000 is goo for you 
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.52.1"  #Change to your local IP, or just put gethostname
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

send("Hello World")
input()
send("Hello Minh") 
input()
send("Hello Everyone!")
send(DISCONNECT_MESSAGE)