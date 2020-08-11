"""Test the SM API wrapper"""

import pytest
import sportmonks
import connection

@pytest.fixture
def _continent_keys():
    """Keys that should be returned by the continent endpoint"""
    return ["id", "name", "countries"]


def test_continent_keys(_continent_keys):
    """Tests the API call to get continent info"""

    response = sportmonks.get_continents(includes="countries")
    assert isinstance(response, list), "not a list"
    n = len(response)
    for i in response:
        assert isinstance(i, dict), "not a dict"
    for i in range(n):
        for j in range(i+1, n):
            assert response[i].keys() == response[j].keys(), \
            "All dictionaries should have the same keys"
    assert set(_continent_keys).issubset(response[0].keys()), "All keys should be in the response"

def test_unnest():
    """
    Test the unnesting function
    """
    assert connection.unnest_includes({"hi": {"data": [1, 2]}}) == {"hi" : [1, 2]}
