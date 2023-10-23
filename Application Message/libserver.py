import sys
import socket
import selectors
import types

class Message:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._jsonheader_len = None
        self._jsonheader = None
        self.request = None
        self.response_created = False

    def _read(self): # Read Logic
        pass

    def _write(self): # Write Logic
        pass

    def process_protoheader(self): #Process Protocol Header
        pass

    def process_jsonheader(self): #JSON Header
        pass

    def process_request(self): #Request
        pass

    def create_response(self): #Response
        pass

    def read(self):
        self._read()

        if self._jsonheader_len is None:
            self.process_protoheader()
        
        if self._jsonheader_len is not None:
            if self._jsonheader is None:
                self.process_jsonheader()
        
        if self._jsonheader:
            if self.request is None:
                self.process_request()
    
    def write(self):
        if self.request:
            if not self.response_created:
                self.create_response()

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()
