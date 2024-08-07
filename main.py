import os
import socket
from dotenv import load_dotenv
from core.logger import Logger

# Initialize Logger
logger = Logger(__name__).get_logger()

# Load .env file
dotenv_path = ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

from server.app import app

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception as e:
        logger.error(f"Error obtaining local IP: {e}")
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    try:
        import uvicorn
        local_ip = get_local_ip()
        logger.info(f"Current local IP address: {local_ip}")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        logger.error(f"An error occurred: {e}")