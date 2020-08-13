"""Test the SM API wrapper"""
import os
import sys
import inspect
import unittest
from unittest import mock
import requests
import requests_mock

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import sportmonks as sm
import helper
from connection import get_data
