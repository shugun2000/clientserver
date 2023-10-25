import sys
import asyncio
from libserver import Message

async def accept_wrapper(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Accepted connection from {addr}")
    message = Message(reader, writer, addr)
    asyncio.create_task(message.process_events())

async def start_server(host, port):
    server = await asyncio.start_server(
        accept_wrapper, host, port)

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    host = '10.1.2.138'
    port = 65432
    asyncio.run(start_server(host, port))
