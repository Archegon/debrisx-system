from core.logger import Logger

# Create a logger instance
logger = Logger(__name__).get_logger()

# Log some messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")