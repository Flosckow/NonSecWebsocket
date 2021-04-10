import asyncio
import websockets
from WebsocketChat.server import Server


async def produce(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as ws:
        await ws.send(message)
        await ws.recv()


# ЗАПУСК СЕРВЕРА
if __name__ == '__main__':
    server = Server(USERS=('Dani'))
    start_server = websockets.serve(server.ws_handler, 'localhost', 4000)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
