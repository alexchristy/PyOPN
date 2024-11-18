from typing import Optional
from pyopnsense.base_namespace import BaseNamespace

# Import the client class
from pyopnsense.dhcpv4 import ServiceClient


class Dhcpv4Namespace(BaseNamespace):
    """Namespace for Dhcpv4-related API clients."""

    # Internal attribute for lazy initialization
    _service: Optional[ServiceClient] = None

    @property
    def service(self) -> ServiceClient:
        if not self._service:
            self._service = self._initialize_client("service", ServiceClient)
        return self._service
