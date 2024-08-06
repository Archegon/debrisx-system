import asyncio
import os
import websockets
from core.logger import Logger
from central import boat
from modules.collector.servo import ServoController

# Initialize Logger
logger = Logger(__name__).get_logger()

# Load WebSocket URL from environment variable
BACKEND_IP = os.getenv('BACKEND_IP')
logger.info(f"BACKEND_IP env: {BACKEND_IP}")

if not BACKEND_IP:
    raise EnvironmentError("BACKEND_IP environment variable not set")

# Variable to track the last servo command time
last_servo_command_time = 0
SERVO_COMMAND_LIMIT = 1  # Limit servo commands to once per second

async def listen():
    global last_servo_command_time
    url = f"ws://{BACKEND_IP}/ws?client=raspberry"
    motor_controller = boat.motor_controller
    servo_controller = boat.servo_controller

    while True:
        try:
            logger.info(f"Connecting to {url}")
            async with websockets.connect(url) as websocket:
                logger.info("Connected to WebSocket")
                sensor_task = asyncio.create_task(send_sensor_data(websocket, boat))
                while True:
                    try:
                        message = await websocket.recv()
                        logger.info(f"Received message: {message}")
                        await handle_message(message, motor_controller, servo_controller)
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

async def handle_message(message, motor_controller, servo_controller):
    global last_servo_command_time
    current_time = asyncio.get_event_loop().time()
    
    if message == "FORWARD":
        motor_controller.forward()
        logger.info("Motor moving forward")
    elif message == "BACKWARD":
        motor_controller.backward()
        logger.info("Motor moving backward")
    elif message == "LEFT":
        motor_controller.turn_left()
        logger.info("Motor turning left")
    elif message == "RIGHT":
        motor_controller.turn_right()
        logger.info("Motor turning right")
    elif message == "STOP":
        motor_controller.stop()
        logger.info("Motor stopped")
    elif message.startswith("SERVO:"):
        if current_time - last_servo_command_time >= SERVO_COMMAND_LIMIT:
            try:
                angle = int(message.split(":")[1])
                await servo_controller.set_angle(angle)
                logger.info(f"Set servo angle to {angle}")
                last_servo_command_time = current_time
            except ValueError:
                logger.error(f"Invalid servo angle: {message}")
            except AngleOutOfRangeError as e:
                logger.error(f"Servo angle out of range: {e}")
        else:
            logger.info(f"Servo command rate limited. Command ignored: {message}")
    else:
        logger.warning(f"Unknown command: {message}")

if __name__ == "__main__":
    try:
        asyncio.run(listen())
    except KeyboardInterrupt:
        logger.info("Program stopped by User")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)

async def send_sensor_data(websocket, boat_controller):
    while True:
        try:
            sensor_data_json = await boat_controller.read_sensors()
            if sensor_data_json:
                await websocket.send(f"SENSOR_DATA:{sensor_data_json}")
                logger.info(f"Sent sensor data: {sensor_data_json}")
            await asyncio.sleep(2)  # Send data every 2 seconds
        except Exception as e:
            logger.error(f"Error sending sensor data: {e}")
            break