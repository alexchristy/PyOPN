from typing import Optional
from pyopnsense.base_namespace import BaseNamespace

# Import the client class
from pyopnsense.core.dhcpv4 import ServiceClient, LeasesClient


class Dhcpv4Namespace(BaseNamespace):
    """Namespace for Dhcpv4-related API clients."""

    # Internal attribute for lazy initialization
    _service: Optional[ServiceClient] = None
    _leases: Optional[LeasesClient] = None

    @property
    def service(self) -> ServiceClient:
        if not self._service:
            self._service = self._initialize_client("service", ServiceClient)
        return self._service

    @property
    def leases(self) -> LeasesClient:
        if not self._leases:
            self._leases = self._initialize_client("leases", LeasesClient)
        return self._leases