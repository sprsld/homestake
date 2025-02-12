import logging

# Create a logger
logger = logging.getLogger("homestake_logger")
logger.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler("homestake.log")
handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(handler)
