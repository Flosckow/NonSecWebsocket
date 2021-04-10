import logging
import asyncio
from websockets import WebSocketClientProtocol

logging.basicConfig(level=logging.INFO)


class Server:

    def __init__(self, USERS):
        self.USERS = set()

    clients = set()

    async def add_user(self, ws: WebSocketClientProtocol):
        self.USERS.add(ws)

    async def remove_user(self, ws: WebSocketClientProtocol):
        self.USERS.remove(ws)

    async def register(self, ws: WebSocketClientProtocol):
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connect')

    async def unregister(self, ws: WebSocketClientProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnect')

    async def send_to_clients(self, message: str):
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def ws_handler(self, ws: WebSocketClientProtocol, uri: str):
        await self.add_user(ws)
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)

        try:
            while True:
                message = await ws.recv()

                await asyncio.wait([user.send(message) for user in self.USERS])
        finally:
            await self.remove_user(ws)

    async def distribute(self, ws: WebSocketClientProtocol):
        async for message in ws:
            await self.send_to_clients(message)




