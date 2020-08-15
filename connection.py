"""
Connect to the SportMonks API.
 """
import os
import logging
import requests
import helper
from errors import (
    BadRequest,
    UnathourizedRequest,
    APIPermissionError,
    APINotFound,
    TooManyRequests,
    ServerErrors
)

log = helper.setup_logger(__name__, "SM_API.log")

API_CODE = os.environ.get("SportMonks_API_KEY")
API_URL = "https://soccer.sportmonks.com/api/v2.0/"
TIMEZONE = "GMT+1"


def get_data(endpoint: str, includes: str = None, params: dict = None):
    """
    Fetches data from SportMonks API.

    Args:
        endpoint:
            SportMonks API endpoint.
        includes: optional
            SportMonks API includes
        params: optional
            Paramaters to add the the URL for filtering purposes.

    Returns:
        Parsed HTTP response from SportMonks API.
        JSON format.
    """

    payload = {"api_token": API_CODE, "tz": TIMEZONE}

    if params:
        for k in params.keys():
            if isinstance(params[k], list):
                params[k] = ",".join(list(map(str, params[k])))
        payload.update(params)

    if includes:
        log.info("Includes specified: %s", includes)
        payload["include"] = includes

    if "page" not in payload:
        payload["page"] = 1

    log.info("Paramaters to filter/query by: %s", params)

    r = requests.get(API_URL + endpoint, params=payload)
    log.info("requets.get: %s", r)
    log.debug("Made request, status code: %s", r.status_code)
    log.info("URL: %s", r.url)

    response = r.json()
    log.info("Response JSON: %s", response)

    if "error" in response:
        error_message = response["error"]["message"]
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
            raise TooManyRequests(f"You have reached your request limit, reason: {error_message}")
        elif r.status_code in [500, 502, 503, 504]:
            raise ServerErrors(f"Server errors, reason: {error_message}")

    if  ("meta" in response \
        and "pagination" in response["meta"] \
        and (response["meta"]["pagination"]["current_page"] <
             response["meta"]["pagination"]["total_pages"]) \
        and response["meta"]["pagination"]["current_page"] == 1):

        log.info("Response is paginated: %s pages", response["meta"]["pagination"]["total_pages"])

        for page_number in range(2, response["meta"]["pagination"]["total_pages"] + 1):
            payload["page"] = page_number
            r_page = get_data(endpoint, includes=includes, params=payload)
            response["data"] += r_page


    if "data" in response:
        response = response["data"]
        log.info("Response is of type: %s", type(response))
        if isinstance(response, dict):
            log.info("Response is a dict, Keys: %s", response.keys())
        elif isinstance(response, list) and response != []:
            log.info("Response is a list of dicts, Keys: %s", response[0].keys())
        else:
            log.info("Response is %s", response)

    if isinstance(response, dict):
        response = helper.unnest_includes(response)
    elif isinstance(response, list):
        response = [helper.unnest_includes(d) for d in response]
    else:
        raise TypeError(f"Can't unnest an object of type: {type(response)}")

    return response
