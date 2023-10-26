import sys
import socket
import selectors
import struct
import json

class Message:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._jsonheader_len = None
        self._jsonheader = None
        self.request = None
        self.response_created = False
        self._recv_buffer = b""
        self._send_buffer = b""

    def create_response(self):
        if self.jsonheader["content-type"] == "text/json":
            response_data = {"message": "Your JSON response data here"}
            response = self._create_response_json_content(response_data)
        else:
            response_data = b"Your binary response data here"
            response = self._create_response_binary_content(response_data)
        message = self._create_message(**response)
        self.response_created = True
        self._send_buffer += message

    def _create_response_json_content(self, response_data):
        response_data = json.dumps(response_data).encode("utf-8")
        return {
            "content-type": "text/json",
            "content-encoding": "utf-8",
            "content-length": len(response_data),
            "response_data": response_data,
        }

    def _create_response_binary_content(self, response_data):
        return {
            "content-type": "binary",
            "content-length": len(response_data),
            "response_data": response_data,
        }

    def _create_message(self, **response):
        jsonheader = json.dumps(response).encode("utf-8")
        header = struct.pack(">H", len(jsonheader))
        return header + jsonheader

    def _write(self):
        if self._send_buffer:
            try:
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                if sent and not self._send_buffer:
                    self.close()

    def _read(self):
        pass

    def process_protoheader(self):
        hdrlen = 2
        if len(self._recv_buffer) >= hdrlen:
            self._jsonheader_len = struct.unpack(">H", self._recv_buffer[:hdrlen])[0]
            self._recv_buffer = self._recv_buffer[hdrlen:]

    def write(self):
        if self.request:
            if not self.response_created:
                self.create_response()

    def process_jsonheader(self):
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            self.jsonheader = json.loads(self._recv_buffer[:hdrlen].decode("utf-8"))
            self._recv_buffer = self._recv_buffer[hdrlen:]
            for reqhdr in ["byteorder", "content-length", "content-type", "content-encoding"]:
                if reqhdr not in self.jsonheader:
                    raise ValueError(f"Missing required header '{reqhdr}'.")

    def process_request(self):
        content_len = self.jsonheader["content-length"]
        if len(self._recv_buffer) >= content_len:
            data = self._recv_buffer[:content_len]
            self._recv_buffer = self._recv_buffer[content_len:]
            if self.jsonheader["content-type"] == "text/json":
                encoding = self.jsonheader["content-encoding"]
                self.request = json.loads(data.decode(encoding))
                print(f"Received request {self.request!r} from {self.addr}")
            else:
                self.request = data
                print(f"Received {self.jsonheader['content-type']} Request from {self.addr}")
                self._set_selector_events_mask("w")

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def close(self):
        print(f"Closing connection to {self.addr}")
        self.selector.unregister(self.sock)
        self.sock.close()

    def read(self):
        pass

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    sock.setblocking(False)
    message = Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)

if __name__ == '__main__':
    sel = selectors.DefaultSelector()

    host = "127.0.0.1"
    port = 65432
    addr = (host, port)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(addr)
    server.listen()
    server.setblocking(False)

    sel.register(server, selectors.EVENT_READ, data=None)

    print(f"Server listening on {host}:{port}")

    try:
        while True:
            events = sel.select()
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
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
