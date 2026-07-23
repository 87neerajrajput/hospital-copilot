import logging

from config.settings import DEBUG


LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)


logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format=LOG_FORMAT,
)


def get_logger(name: str):

    return logging.getLogger(name)