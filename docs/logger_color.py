import logging
from colorlog import ColoredFormatter

# Create a custom formatter with color
formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)

# Configure the logger
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger("example")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Example log messages
logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")
