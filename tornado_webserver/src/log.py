import logging
from logging.handlers import SysLogHandler
import os

PAPERTRAIL_HOST: str = os.environ["PAPERTRAIL_HOST"]
PAPERTRAIL_PORT: int = int(os.environ["PAPERTRAIL_PORT"])


def logging_func(logger_name: str, level: int) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)  # logging.DEBUG
    handler = SysLogHandler(address=(PAPERTRAIL_HOST, PAPERTRAIL_PORT))
    logger.addHandler(handler)
    return logger


def main() -> None:
    logger = logging_func("dora", logging.INFO)
    logger.debug("I am a debug message")


if __name__ == "__main__":
    main()
