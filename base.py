"""
Implement OOP ideas in to my sportmonks module.
API information: https://www.sportmonks.com/products/soccer
 """
import os
import logging
from datetime import datetime
import time
from typing import Dict, Optional, Union, List, Any
import pandas as pd
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

class BaseAPI(object):
    """Base API for SportMonks"""

    def __init__(self, api_key: str = None, timeout: int = 2,
                 tz: Optional[str] = None):

        self.url = "https://soccer.sportmonks.com/api/v2.0/"
        self.api_key = api_key
        self.timeout = timeout

        if tz:
            self.tz = tz
        else:
            self.tz = datetime.now().astimezone().tzinfo

        self.get_key()
        self.initial_params = {"api_token": self.api_key, "tz": self.tz}
        self.meta_info()

        if tz:
            self.tz = tz
        else:
            self.tz = datetime.now().astimezone().tzinfo

    def get_key(self):
        """
        If no api_key is specified, then look in environment variables
        for the key called "SPORTMONKS_KEY".
        """

        if self.api_key is None:
            if os.environ.get("SPORTMONKS_KEY"):
                self.api_key = os.environ.get("SPORTMONKS_KEY")
            else:
                raise APIKeyMissing("Make an environment variable named 'SPORTMONKS_KEY' \
                                    to store your api key")

    def meta_info(self):
        """Returns meta info from your SportMonks plan."""

        r = requests.get(self.create_api_url(endpoint="continents"),
                         params=self.initial_params).json()
        plan = r.get("meta").get("plan")

        if plan:
            self.plan_name = plan.get("name")
            self.plan_price = "\u20ac" + plan.get("price")
            limit, mins = plan.get("request_limit").split(",")
            self.request_limit = f"{limit} requests per {mins} minutes."

        return None

    @property
    def headers(self):
        """Headers"""
        if self.tz:
            return {"Content-Type": "application/json",
                    "Accept": "application/json",
                    "Accept-Encoding": "deflate, gzip",
                    "Date": f"{datetime.now(pytz.timezone(self.tz))}"}
        else:
            return {"Content-Type": "application/json",
                    "Accept": "application/json",
                    "Accept-Encoding": "deflate, gzip",
                    "Date": f"{datetime.now()}"}

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

    def create_api_url(self, endpoint: Union[str, int, List[str, int]]):
        """
        Creates API URL for different endpoints.
        Excludes paramaters which are passed in to request.get().
        """
        endpoint = [endpoint] if isinstance(endpoint, (str, int)) else endpoint

        return self.url + "/".join(list(map(str, endpoint)))
        """
        if isinstance(endpoint, str):
            return self.url + endpoint
        elif isinstance(endpoint, list):
            return self.url + "/".join(list(map(str, endpoint)))
        else:
            raise TypeError(f"Did not expect endpoint of type: {type(endpoint)}")"""

    @staticmethod
    def process_includes(includes: Union[str, List[str]]):
        """
        includes must be in the form of a string,
        with the include separated by a comma.
        """
        includes = [includes] if isinstance(includes, str) else includes
        return ",".join(includes)

    @staticmethod
    def process_params(params: dict):
        """
        Processes the paramaters ready to be put in to the query string.
        """
        for key in params.keys():
            if isinstance(params[key], list):
                params[key] = ",".join(list(map(str, params[key])))

        return params

    def make_request(self, endpoint: Union[str, List[str]],
                     includes: Optional[List[str]] = None,
                     params: Optional[dict] = None):

        """Make a GET reqeust to SportMonks API"""

        if params:
            params = self.process_params(params)
            params.update(self.initial_params)
        else:
            params = self.initial_params

        if includes:
            includes = self.process_includes(includes)
            params["include"] = includes

        if "page" not in params:
            params["page"] = 1

        url = self.create_api_url(endpoint=endpoint)

        try:
            r = requests.get(url, params=params, headers=self.headers,
                             timeout=self.timeout)
            log.info("URL: %s", r.url)
        except requests.exceptions.Timeout as e:
            log.info("Response has timed out: %s", e)
            raise SystemExit(e)
            # recursion here?

        try:
            response = r.json()
            log.info("response: %s", response)
        except ValueError as e:
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

        data = response.get("data")
        if not data:
            log.error("No data was included!")
            return None

        if "pagination" in response.get("meta"):
            total_pages = response["meta"]["pagination"].get("total_pages")
            log.info("Response is paginated; %s pages", total_pages)
            for page in range(2, total_pages + 1):
                params["page"] = page
                r = requests.get(url, params=params, headers=self.headers,
                                 timeout=self.timeout)
                log.info("URL: %s", r.url)
                next_page_data = r.json().get("data")
                if next_page_data:
                    data += next_page_data

        if isinstance(data, dict):
            data = self.unnest_includes(data)
        elif isinstance(data, list):
            data = [self.unnest_includes(d) for d in data]
        else:
            raise TypeError(f"Did not expect response of type: {type(data)}")

        return data
