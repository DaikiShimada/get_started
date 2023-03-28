from __future__ import annotations

import logging
from typing import Optional

__all__ = ["loglevels", "get_loglevel", "get_logger"]


_LOG_LEVEL = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


def loglevels() -> list[str]:
    return list(_LOG_LEVEL.keys())


def get_loglevel(s: str) -> int:
    assert s in _LOG_LEVEL, "Unknown loglevel: %s" % s
    return _LOG_LEVEL[s.lower()]


def get_logger(
    name: Optional[str] = __name__,
    output: Optional[str] = None,
    stream_level: str = "info",
    file_level: str = "info",
) -> logging.Logger:
    if name is None:
        # getting root logger
        logger = logging.getLogger(name)
    else:
        logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(get_loglevel(stream_level))
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s | %(message)s")
    handler.setFormatter(formatter)
    handler.setLevel(0)
    logger.addHandler(handler)

    if output is not None:
        file_handler = logging.FileHandler(output, mode="w")
        file_handler.setLevel(get_loglevel(file_level))
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
