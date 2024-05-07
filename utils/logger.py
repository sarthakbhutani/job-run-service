from utils.settings import SERVICE_NAME,LOG_LEVEL
import logging

def setup_logger():
    """Set up the logger."""
    extra = {"app_name": SERVICE_NAME}
    logging.basicConfig(level=logging.INFO, format="%(asctime)s HyperExecute Service: %(message)s", force=True)
    logger = logging.getLogger(__name__)
    logger = logging.LoggerAdapter(logger, extra)
    logger.setLevel(logging.getLevelName(LOG_LEVEL))
    return logger

log_my_ass = True