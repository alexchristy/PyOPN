from typing import Optional, cast

from pyopn.base_namespace import BaseNamespace

# Import the client class
from pyopn.core.kea import CtrlAgentClient, Dhcpv4Client, Leases4Client, ServiceClient


class KeaNamespace(BaseNamespace):
    """Namespace for Kea related API clients."""

    # Internal attribute for lazy initialization
    _ctrl_agent: Optional[CtrlAgentClient] = None
    _dhcpv4: Optional[Dhcpv4Client] = None
    _leases4: Optional[Leases4Client] = None
    _service: Optional[ServiceClient] = None

    @property
    def ctrl_agent(self) -> CtrlAgentClient:
        """Access the Kea ctrl_agent controller."""
        if not self._ctrl_agent:
            self._ctrl_agent = self._initialize_client("ctrl_agent", CtrlAgentClient)
        return cast(CtrlAgentClient, self._ctrl_agent)

    @property
    def dhcpv4(self) -> Dhcpv4Client:
        """Access the Kea dhcpv4 controller."""
        if not self._dhcpv4:
            self._dhcpv4 = self._initialize_client("dhcpv4", Dhcpv4Client)
        return cast(Dhcpv4Client, self._dhcpv4)

    @property
    def leases4(self) -> Leases4Client:
        """Access the Kea leases4 controller."""
        if not self._leases4:
            self._leases4 = self._initialize_client("leases4", Leases4Client)
        return cast(Leases4Client, self._leases4)

    @property
    def service(self) -> ServiceClient:
        """Access the Kea service controller."""
        if not self._service:
            self._service = self._initialize_client("service", ServiceClient)
        return cast(ServiceClient, self._service)
