"""Custom Exceptions"""

class BadRequest(Exception):
    """Status code: 400"""

class UnathourizedRequest(Exception):
    """Status code 401; invalid API key"""

class APIPermissionError(Exception):
    """Staus code 403; insufficient privileges."""

class APINotFound(Exception):
    """Status code: 404"""

class TooManyRequests(Exception):
    """Status code: 429"""

class ServerErrors(Exception):
    """Status codes: 500, 502, 503, 504"""
