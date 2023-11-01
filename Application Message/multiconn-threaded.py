import socket
import threading

def threaded(c):
    while True:
        data = c.recv(1024)
        if not data:
            print('Bye')
            break

        data = data[::-1]

        c.send(data)

    c.close()

def Main():
    host = '127.0.0.1'  # The host should be a string
    port = 65432
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Socket bound to port", port)
    s.listen(5)
    print("Socket is listening")
    
    while True:
        c, addr = s.accept()
        print('Connected to:', addr[0], ':', addr[1])
        threading.Thread(target=threaded, args=(c,)).start()

if __name__ == '__main__':
    Main()
