import asyncio
import websockets
import os

WS_URL = os.getenv('WS_URL')
print(f"WS_URL env: {WS_URL}")

if not WS_URL:
    raise EnvironmentError("WS_URL environment variable not set")

async def listen():
    uri = f"ws://{WS_URL}/ws?client=raspberry"
    while True:
        try:
            print(f"Connecting to {uri}")
            async with websockets.connect(uri) as websocket:
                print("Connected to WebSocket")
                while True:
                    try:
                        message = await websocket.recv()
                        print(f"Received message: {message}")
                    except websockets.exceptions.ConnectionClosed as e:
                        print(f"Connection closed with error: {e}")
                        break
        except (websockets.exceptions.ConnectionClosedError, 
                websockets.exceptions.InvalidURI, 
                websockets.exceptions.InvalidHandshake, 
                OSError) as e:
            print(f"Connection attempt failed: {e}")
        
        print("Retrying connection in 5 seconds...")
        await asyncio.sleep(5)  # Delay before retrying