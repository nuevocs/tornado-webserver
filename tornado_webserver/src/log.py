import logging
from logging.handlers import SysLogHandler

PAPERTRAIL_HOST = 'logs3.papertrailapp.com'
PAPERTRAIL_PORT = 27543


def logging_func(logger_name: str, level: int) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)  # logging.DEBUG
    handler = SysLogHandler(address=(PAPERTRAIL_HOST, PAPERTRAIL_PORT))
    logger.addHandler(handler)
    return logger


def main() -> None:
    # logger = logging.getLogger("Tat")
    # logger.setLevel(logging.DEBUG)
    # handler = SysLogHandler(address=(PAPERTRAIL_HOST, PAPERTRAIL_PORT))
    # logger.addHandler(handler)
    # logger.debug("I am a debug message")
    # logger.info("I am an info message")

    logger = logging_func("dora", logging.INFO)
    logger.debug("I am a debug message")


if __name__ == "__main__":
    main()
