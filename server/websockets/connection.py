import asyncio
import os
import websockets
from core.logger import Logger
from central import RCBoatController
import pigpio

# Initialize Logger
logger = Logger(__name__).get_logger()

# Load WebSocket URL from environment variable
WS_URL = os.getenv('WS_URL')
logger.info(f"WS_URL env: {WS_URL}")

if not WS_URL:
    raise EnvironmentError("WS_URL environment variable not set")

async def listen():
    url = f"ws://{WS_URL}/ws?client=raspberry"
    pi = pigpio.pi()
    motor_controller = RCBoatController.motor_controller

    while True:
        try:
            logger.info(f"Connecting to {url}")
            async with websockets.connect(url) as websocket:
                logger.info("Connected to WebSocket")
                while True:
                    try:
                        message = await websocket.recv()
                        logger.info(f"Received message: {message}")
                        handle_message(message, motor_controller)
                    except websockets.exceptions.ConnectionClosed as e:
                        logger.error(f"Connection closed with error: {e}")
                        break
        except (websockets.exceptions.ConnectionClosedError, 
                websockets.exceptions.InvalidURI, 
                websockets.exceptions.InvalidHandshake, 
                OSError) as e:
            logger.error(f"Connection attempt failed: {e}")
        
        logger.info("Retrying connection in 5 seconds...")
        await asyncio.sleep(5)  # Delay before retrying

def handle_message(message, motor_controller):
    if message == "forward":
        motor_controller.move_forward()
        logger.info("Motor moving forward")
    elif message == "backward":
        motor_controller.move_backward()
        logger.info("Motor moving backward")
    elif message == "left":
        motor_controller.turn_left()
        logger.info("Motor turning left")
    elif message == "right":
        motor_controller.turn_right()
        logger.info("Motor turning right")
    elif message == "stop":
        motor_controller.stop()
        logger.info("Motor stopped")
    else:
        logger.warning(f"Unknown command: {message}")

if __name__ == "__main__":
    try:
        asyncio.run(listen())
    except KeyboardInterrupt:
        logger.info("Program stopped by User")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
