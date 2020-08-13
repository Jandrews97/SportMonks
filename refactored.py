"""
Implement OOP ideas in to my sportmonks module.
API information: https://www.sportmonks.com/products/soccer
 """
import os
import logging
from datetime import datetime
from typing import Dict, Optional, Union, List, Any
import requests
import pytz
import errors
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

    def get_key(self):
        """
        If no api_key is specified, then look in environment variables
        for the key called key_name
        """

        if self.api_key is None:
            if os.environ.get("SPORTMONKS_KEY"):
                self.api_key = os.environ.get("SPORTMONKS_KEY")
            else:
                raise errors.APIKeyMissing("API key is missing")

    @property
    def headers(self, tz: str):
        """Headers"""
        return {"Content-Type": "application/json",
                "Accept": "application/json",
                "Accept-Encoding": "deflate, gzip",
                "Date": f"{datetime.now(pytz.timezone(tz))}"}

    @property
    def params(self, api_key: str, tz: str):
        """Initial paramaters"""
        return {"api_token": api_key, "tz": tz}
