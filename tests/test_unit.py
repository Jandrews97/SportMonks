"""Test the SM API wrapper"""

import os
import unittest
from unittest.mock import Mock, patch
import pytest
import requests
from base import BaseAPI

from errors import (
    BadRequest,
    UnathourizedRequest,
    APIPermissionError,
    APINotFound,
    TooManyRequests,
    ServerErrors,
    APIKeyMissing,
)

class TestBase(unittest.TestCase):

    def setUp(self):

        self.base = BaseAPI(api_key="foo")

    @patch("base.requests.get")
    def test_exceptions(self, mock_get):

        error_status_codes = {
            BadRequest: 400,
            UnathourizedRequest: 401,
            APIPermissionError: 403,
            APINotFound: 404,
            TooManyRequests: 429,
            ServerErrors: [500, 502, 503, 504]
        }

        mock_response = Mock()
        expected_response = {"data": {"foo": "bar"}, "error": {"foo": "bar"}}
        mock_response.json.return_value = expected_response
        mock_get.return_value = mock_response

        for exception in error_status_codes:
            mock_response.status_code = error_status_codes[exception]
            if isinstance(error_status_codes[exception], list):
                for code in error_status_codes[exception]:
                    mock_response.status_code = code
                    self.assertRaises(exception, self.base.make_request, "foo")
                continue

            self.assertRaises(exception, self.base.make_request, "foo")

    @patch("base.requests.get")
    def test_successful_call(self, mock_get):

        mock_response = Mock()
        expected_response = {"data": {"foo":"bar"}}
        mock_response.json.return_value = expected_response
        mock_get.return_value = mock_response

        response_dict = self.base.make_request("foo")

        mock_get.assert_called_once()
        self.assertEqual(1, mock_response.json.call_count)
        self.assertEqual({"foo": "bar"}, response_dict)

    @patch("base.requests.get")
    def test_args(self, mock_get):

        self.base.timeout = 10

        mock_response = Mock()
        expected_response = {"data": {"foo":"bar"}}
        mock_response.json.return_value = expected_response
        mock_get.return_value = mock_response

        for endpoint in ["foo", "bar", ["foo", "bar"]]:

            if isinstance(endpoint, list):
                endpoint = ",".join(endpoint)

            url = 'https://soccer.sportmonks.com/api/v2.0/'+ endpoint

            self.base.make_request(endpoint, includes="foo")
            print(mock_get.call_args[1])
            self.assertEqual(mock_get.call_args[0][0], url)
            self.assertEqual(mock_get.call_args[1]["timeout"], 10)
            self.assertEqual(mock_get.call_args[1]["params"].get("include"), "foo")


if __name__ == "__main__":
    unittest.main()
