import asyncio
import websockets
import os

BACKEND_IP = os.getenv('BACKEND_IP')
print(f"BACKEND_IP env: {BACKEND_IP}")

if not RPI_IP:
    raise EnvironmentError("BACKEND_IP environment variable not set")

async def listen():
    uri = f"ws://{BACKEND_IP}/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")

asyncio.get_event_loop().run_until_complete(listen())