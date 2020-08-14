"""
Implement OOP ideas in to my sportmonks module.
API information: https://www.sportmonks.com/products/soccer
 """
import os
import logging
from datetime import datetime
import time
from typing import Dict, Optional, Union, List, Any
import json
import requests
import pytz
from errors import (
    BadRequest,
    UnathourizedRequest,
    APIPermissionError,
    APINotFound,
    TooManyRequests,
    ServerErrors,
    APIKeyMissing
)
import helper

log = helper.setup_logger(__name__, "SM_API.log")

class API(object):
    """Base API for SportMonks"""

    def __init__(self, api_key: str = None, timeout: int = 2,
                 tz: Optional[str] = None):

        self.url = "https://soccer.sportmonks.com/api/v2.0/"
        self.api_key = api_key
        self.timeout = timeout
        self.tz = tz
        self.get_key()
        self.initial_params = {"api_token": self.api_key, "tz": self.tz}

    def get_key(self):
        """
        If no api_key is specified, then look in environment variables
        for the key called "SPORTMONKS_KEY".
        """

        if self.api_key is None:
            if os.environ.get("SPORTMONKS_KEY"):
                self.api_key = os.environ.get("SPORTMONKS_KEY")
            else:
                raise APIKeyMissing("API key is missing")

    @property
    def headers(self):
        """Headers"""
        return {"Content-Type": "application/json",
                "Accept": "application/json",
                "Accept-Encoding": "deflate, gzip",
                "Date": f"{datetime.now(pytz.timezone(self.tz))}"}


    def unnest_includes(self, dictionary: dict):
        """
            Changes the SportMonks API response to get rid of the
            superfluous "data" that is included inside an includes
            response.
            {...,
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

        {...,
            "season": {
                    "id": 16216,
                    "name": "2019/2020",
                    "league_id": 27,
                    "is_current_season": true,
                    "current_round_id": null,
                    "current_stage_id": 77444688
                }

        }
    """
        unnested = dict()

        for key in dictionary:
            if isinstance(dictionary[key], dict) and list(dictionary[key].keys()) == ["data"]:
                data = dictionary[key]["data"]

                if isinstance(data, list):
                    for i, v in enumerate(data):
                        if isinstance(v, dict):
                            data[i] = self.unnest_includes(v)
                elif isinstance(data, dict):
                    data = self.unnest_includes(data)

                unnested[key] = data

            else:
                unnested[key] = dictionary[key]

        return unnested

    def create_api_url(self, endpoint: Union[str, List[str]]):
        """
        Creates API URL for different endpoints.
        Excludes paramaters which are passed in to request.get().
        """
        if isinstance(endpoint, str):
            return self.url + "/" + endpoint
        elif isinstance(endpoint, list):
            return self.url + "/" + "/".join(endpoint)
        else:
            raise TypeError(f"Did not expect endpoint of type: {type(endpoint)}")

    @staticmethod
    def process_includes(includes: Union[str, List[str]]):
        """
        includes must be in the form of a string,
        with the include separated by a comma.
        """
        includes = [includes] if isinstance(includes, str) else includes
        return ",".join(includes)

    def make_request(self, endpoint: Union[str, List[str]],
                     includes: Optional[List[str]] = None,
                     params: Optional[dict] = None):

        """Make a GET reqeust to SportMonks API"""

        if params:
            payload = self.initial_params.update(params)

        if includes:
            includes = self.process_includes(includes)
            payload["include"] = includes

        url = self.create_api_url(endpoint=endpoint)
        try:
            r = requests.get(url, params=payload, headers=self.headers,
                             timeout=self.timeout)
        except requests.exceptions.Timeout as e:
            log.info("Response has timed out: %s", e)
            raise SystemExit(e)
            # recursion here?

        try:
            response = r.json()
        except json.decoder.JSONDecodeError as e:
            log.info("Could not decode response in to JSON: %s", e)
            raise SystemExit(e)


        if "error" in response:
            error_message = response["error"].get("message")
            log.error("Error: %s", error_message)

            if r.status_code == 400:
                raise BadRequest(f"Bad Request Error, reason: {error_message}")
            elif r.status_code == 401:
                raise UnathourizedRequest(f"Invalid API Key, reason: {error_message}")
            elif r.status_code == 403:
                raise APIPermissionError(f"Permission error, reason: {error_message}")
            elif r.status_code == 404:
                raise APINotFound(f"There is no content, reason: {error_message}")
            elif r.status_code == 429:
                raise TooManyRequests(f"You have reached your request limit, reason: \
                                      {error_message}")
            elif r.status_code in [500, 502, 503, 504]:
                raise ServerErrors(f"Server errors, reason: {error_message}")
