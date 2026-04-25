import logging
from . import  constants


def setup_logging():
    # Only configure if not already configured
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    logger = logging.getLogger(__name__)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    return logger

logger = setup_logging()

def writeLog(message, level="info"):
    # Return early if debug is off to avoid processing
    if not constants.DEBUG:
        return

    # Use standard logging level mapping instead of if/else
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(message)