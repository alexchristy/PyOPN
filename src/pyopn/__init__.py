"""A simple Python wrapper for the OPNsense REST API."""

from pyopn.api import OPNsenseAPI
from pyopn.exceptions import APIError

__all__ = ["APIError", "OPNsenseAPI"]
