import sys
import socket
import selectors
import types

class Message:
    def __init__(self, selector, sock, addr):
        