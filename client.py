import socket

HEADER = 64 # This is 64 bytes that server can handle
PORT = 8080 #THERE ARE 10000 PORT ABOVE 1000 is goo for you 
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.65.1" #Change to your local IP
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)