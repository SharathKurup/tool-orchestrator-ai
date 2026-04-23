import logging
from . import constants

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    return logger


def writeLog(message, level="info"):
    if constants.DEBUG:
        if level == "info":
            logger.info(message)
        elif level == "error":
            logger.error(message)
        elif level == "debug":
            logger.debug(message)

logger = setup_logging()