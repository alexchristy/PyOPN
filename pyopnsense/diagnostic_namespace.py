from typing import Optional
from pyopnsense.base_namespace import BaseNamespace

# Import client classes
from pyopnsense.diagnostics import InterfaceClient, NetFlowClient, NetworkInsightClient, SystemHealthClient


class DiagnosticNamespace(BaseNamespace):
    """Namespace for diagnostic-related API clients."""

    # Internal attributes for lazy initialization
    _interface: Optional[InterfaceClient] = None
    _netflow: Optional[NetFlowClient] = None
    _network_insight: Optional[NetworkInsightClient] = None
    _system_health: Optional[SystemHealthClient] = None

    @property
    def interface(self) -> InterfaceClient:
        if not self._interface:
            self._interface = self._initialize_client("interface", InterfaceClient)
        return self._interface

    @property
    def netflow(self) -> NetFlowClient:
        if not self._netflow:
            self._netflow = self._initialize_client("netflow", NetFlowClient)
        return self._netflow

    @property
    def network_insight(self) -> NetworkInsightClient:
        if not self._network_insight:
            self._network_insight = self._initialize_client("network_insight", NetworkInsightClient)
        return self._network_insight

    @property
    def system_health(self) -> SystemHealthClient:
        if not self._system_health:
            self._system_health = self._initialize_client("system_health", SystemHealthClient)
        return self._system_health