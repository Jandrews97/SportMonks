"""
Helper functions for the Sportmonks module
"""
from typing import Dict, Optional, Union, List, Any
import logging
import json

def unnest_includes(dictionary: dict):
    """
    ***FROM https://github.com/Dmitrii-I/sportmonks/blob/master/sportmonks/_base.py
    Function to tidy up the response when includes and nested includes are used. The response
    from the API is like the below, nested dictionaries:
    {######,
        "season": {
            "data": {
                "id": 16216,
                "name": "2019/2020",
                "league_id": 27,
                "is_current_season": true,
                "current_round_id": null,
                "current_stage_id": 77444688
            }
        }
    }

    Prefer the following:

    {######,
        "season": {
                "id": 16216,
                "name": "2019/2020",
                "league_id": 27,
                "is_current_season": true,
                "current_round_id": null,
                "current_stage_id": 77444688
            }

    }

    Args:
        dictionary:
            The JSON response fromm SportMonks GET request.

    Returns:
        Unnested dictionary.
    """

    unnested = dict()

    for key in dictionary:
        if isinstance(dictionary[key], dict) and list(dictionary[key].keys()) == ["data"]:
            data = dictionary[key]["data"]

            if isinstance(data, list):
                for i, v in enumerate(data):
                    if isinstance(v, dict):
                        data[i] = unnest_includes(v)
            elif isinstance(data, dict):
                data = unnest_includes(data)

            unnested[key] = data
        else:
            unnested[key] = dictionary[key]

    return unnested


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
