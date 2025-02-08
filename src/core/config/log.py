import logging

from pythonjsonlogger.json import JsonFormatter

logger = logging.getLogger(
    __name__,
)
log_handler = logging.StreamHandler()
formatter = JsonFormatter(
    "{asctime} {levelname} {module} {filename} {lineno} {funcName} {message}",
    style="{",
    json_ensure_ascii=False,
)
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)
logging.basicConfig(level="INFO", handlers=[])
