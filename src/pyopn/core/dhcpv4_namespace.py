from typing import Optional, cast

from pyopn.base_namespace import BaseNamespace

# Import the client class
from pyopn.core.dhcpv4 import LeasesClient, ServiceClient


class Dhcpv4Namespace(BaseNamespace):
    """Namespace for Dhcpv4-related API clients."""

    # Internal attribute for lazy initialization
    _service: Optional[ServiceClient] = None
    _leases: Optional[LeasesClient] = None

    @property
    def service(self) -> ServiceClient:
        """Access the ISC DHCPv4 service controller."""
        if not self._service:
            self._service = self._initialize_client("service", ServiceClient)
        return cast(ServiceClient, self._service)

    @property
    def leases(self) -> LeasesClient:
        """Access the ISC DHCPv4 leases controller."""
        if not self._leases:
            self._leases = self._initialize_client("leases", LeasesClient)
        return cast(LeasesClient, self._leases)
