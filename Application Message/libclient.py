import sys
import socket
import selectors
import types

class Message:
    def __init__(self, sock, addr, request=None):
        self.sock = sock
        self.addr = addr
        self._jsonheader_len = None
        self._jsonheader = None
        self.request = request
        self.response_created = False
        self._recv_buffer = b""
        self._send_buffer = b""

    def write(self):
        if not self._request_queued:
            self.queue_request()

        self._write()

        if self._request_queued:
            if not self._send_buffer:
                self._set_selector_events_mask(selectors.EVENT_READ)

    def queue_request(self):
        content = self.request["content"]
        content_type = self.request["type"]
        content_encoding = self.request["encoding"]
        if content_type == "text/json":
            req = {
                "content_bytes": self._json_encode(content, content_encoding),
                "content_type": content_type,
                "content_encoding": content_encoding
            }
        else:
            req = {
                "content_bytes": content,
                "content_type": content_type,
                "content_encoding": content_encoding
            }
            message = self._create_message(**req)
            self._send_buffer += message
            self._request_queued = True

    def process_response(self):
        self.close()

    def _read(self):
        try:
            data = self.sock.recv(4096)
        except BlockingIOError:
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError("Peer closed.")
            

    def _write(self):
        # Implement your write logic here
        pass

    def _set_selector_events_mask(self, mask):
        # Implement setting the selector events mask here
        pass
