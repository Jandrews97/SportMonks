"""
Helper functions for the Sportmonks module.
"""
from typing import Dict, Optional, Union, List, Any
import logging
import json

def setup_logger(name: str, log_file: str, level=logging.DEBUG,
                 fmt: str = "%(name)s -%(asctime)s - %(levelname)s - %(message)s"):
    """
    Setup a logger.

    Args:
        name:
            Name of the logger.
        log_file:
            What file you want to log to.
        level:
            Debugging level. Must be:
            NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL.
        fmt:
            Format of the logger.

    Returns:
        A logger.

    """
    formatter = logging.Formatter(fmt)
    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(file_handler)

    return logger

def to_json(response: Union[Dict, List[Dict]], file: str):
    """
    Writes JSON object from SportMonks API to a json file.
    Aids in visualising the structure.

    Args:
        response:
            JSON object.
        file:
            File you want to write the JSON too.

    Returns:
        None
    """
    with open(file, "w") as f:
        json.dump(response, f)

    return None
