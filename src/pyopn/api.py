import logging
from pathlib import Path
from typing import Any, Optional, Union, cast
from urllib.parse import urlparse

import validators

from pyopn.constants import DEFAULT_TIMEOUT
from pyopn.core.dhcpv4_namespace import Dhcpv4Namespace
from pyopn.core.kea_namespace import KeaNamespace

# Create a module-level logger
logger = logging.getLogger(__name__)


class OPNsenseAPI(object):
    """Wrapper class to manage namespaces and API credentials."""

    def __init__(  # noqa: PLR0913
        self,
        base_url: str,
        api_key_file: Optional[Union[str, Path]] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        verify_cert: bool = False,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        """Initialize OPNsense API object with API key file or API credentials."""
        # Load credentials: Cred file, directly, or throw error
        if api_key_file:
            logger.info("Initializing OPNSenseAPI with API key file.")
            self.api_key, self.api_secret = self._load_keys_from_file(api_key_file)
        elif api_key and api_secret:
            logger.info("Initializing OPNSenseAPI with API key and secret.")
            self.api_key = api_key
            self.api_secret = api_secret
        else:
            logger.error(
                "Initialization failed: Neither api_key_file nor both api_key and api_secret provided."
            )
            msg = "You must provide either an api_key_file path or both api_key and api_secret for initialization."
            raise ValueError(msg)

        if validators.url(base_url):
            self.base_url = self._format_base_url(base_url)
        else:
            msg = f"Provided OPNsense base URL is not valid: {base_url}"
            raise ValueError(msg)

        self.verify_cert = verify_cert
        self.timeout = timeout

        # Lazy initialization of namespaces
        self._namespaces: dict[str, Any] = {}

    def _format_base_url(self, base_url: str) -> str:
        """Ensure that the base_url is properly formatted."""
        base_url = base_url.rstrip("/")

        if not base_url.endswith("/api"):
            parsed_url = urlparse(base_url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/api"

        return base_url

    def _set_credentials(self, api_key: str, api_secret: str) -> None:
        """Update API credentials and invalidate existing namespaces."""
        self.api_key = api_key
        self.api_secret = api_secret
        self._namespaces.clear()

    def _load_keys_from_file(self, file_path: Union[str, Path]) -> tuple[str, str]:
        """Load the API key and secret from a file.

        :param str | Path file_path: Path to the file containing API credentials
        :returns: A tuple containing the API key and secret
        :rtype: tuple[str, str]
        :raises FileNotFoundError: If the file does not exist
        :raises ValueError: If the file contents are invalid or malformed
        """
        path = Path(file_path)
        if not path.is_file():
            logger.error("File not found: %s", file_path)
            msg = f"The file at {file_path} does not exist."
            raise FileNotFoundError(msg)

        logger.debug("Reading API credentials from file: %s", file_path)
        keys = {}
        try:
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        keys[key.strip()] = value.strip().strip('"')  # Remove quotes

            if "key" not in keys or "secret" not in keys:
                logger.error(
                    "Invalid file format in %s: Missing 'key' or 'secret'.", file_path
                )
                msg = "The file must contain both 'key' and 'secret' in the format key=\"value\"."
                raise ValueError(msg)

            logger.info("API credentials successfully loaded from file: %s", file_path)
            return keys["key"], keys["secret"]
        except Exception as e:
            msg = f"Error parsing the API key file: {e}"
            logger.error(msg)
            raise ValueError(msg) from e

    @property
    def dhcpv4(self) -> Dhcpv4Namespace:
        """Access the ISC DHCPv4 module."""
        if "dhcpv4" not in self._namespaces:
            self._namespaces["dhcpv4"] = Dhcpv4Namespace(self)
        return cast(Dhcpv4Namespace, self._namespaces["dhcpv4"])

    @property
    def kea(self) -> KeaNamespace:
        """Access the Kea DHCPv4 module."""
        if "kea" not in self._namespaces:
            self._namespaces["kea"] = KeaNamespace(self)
        return cast(KeaNamespace, self._namespaces["kea"])
