"""Test the SM API wrapper"""

import os
import unittest
from unittest.mock import Mock, patch
import pytest
import requests
from base import BaseAPI
import football

from errors import (
    BadRequest,
    UnathourizedRequest,
    APIPermissionError,
    APINotFound,
    TooManyRequests,
    ServerErrors,
    APIKeyMissing,
    NotJSONNormalizable
)

KEY = os.environ.get("SPORTMONKS_KEY")

class TestBase(unittest.TestCase):

    def setUp(self):

        self.base = BaseAPI(KEY)

    @patch("base.requests.get")
    def test(self, mock_get):

        mock_response = Mock()
        mock_response.status_code = 404
        expected_response = {"data": {"hi": "boo"}, "error": {"woops": "error"}}
        mock_response.json.return_value = expected_response

        mock_get.return_value = mock_response
        #response_dict = self.base.make_request("countries")

        self.assertRaises(APINotFound, self.base.make_request, "countries")

if __name__ == "__main__":
    unittest.main()
