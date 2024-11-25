"""A simple Python wrapper for the OPNsense REST API."""

from .api import OPNsenseAPI
from .exceptions import APIError

__all__ = ["APIError", "OPNsenseAPI"]
