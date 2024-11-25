# Copyright 2024 Alex Christy
#
# This file is part of pyopn
#
# pyopn is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyopn is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyopn. If not, see <http://www.gnu.org/licenses/>.

from typing import Any

from validators import ValidationError, ip_address

from pyopn import client


class ServiceClient(client.OPNClient):
    """A client for interacting with the dhcpv4/service endpoint.

    :param str api_key: The API key to use for requests
    :param str api_secret: The API secret to use for requests
    :param str base_url: The base API endpoint for the OPNsense deployment
    """

    def reconfigure(self, data: dict[str, Any]) -> NotImplementedError:
        """Reconfigure the Dhcpv4 service."""
        msg = "This ISC DHCPv4 endpoint is non-functional see Kea DHCP."
        raise NotImplementedError(msg)
        return self._post("dhcpv4/service/reconfigure", data)

    def restart(self) -> dict[str, Any]:
        """Restart the ISC DHCPv4 service."""
        return self._post("dhcpv4/service/restart", "")

    def start(self) -> dict[str, Any]:
        """Start the ISC DHCPv4 service."""
        return self._post("dhcpv4/service/restart", "")

    def status(self) -> dict[str, Any]:
        """Return the status of the ISC Dhcvpv4 service."""
        return self._get("dhcpv4/service/status")

    def stop(self) -> dict[str, Any]:
        """Stop the ISC Dhcpv4 service."""
        return self._post("dhcpv4/service/stop", "")


class LeasesClient(client.OPNClient):
    """A client for interacting with the dhcpv4/leases endpoint.

    :param str api_key: The API key to use for requests
    :param str api_secret: The API secret to use for requests
    :param str base_url: The base API endpoint for the OPNsense deployment
    """

    def del_lease(self, ip: str) -> dict[str, Any]:
        """Delete lease in ISC DHCPv4 server."""
        if not ip_address.ipv4(ip):
            msg = f"Failed to delete DHCP IP lease. Invalid IP provided: {ip}"
            raise ValidationError(msg)
        return self._post(f"dhcpv4/leases/delLease/{ip}", "")

    def search_lease(self) -> dict[str, Any]:
        """Return all leases in the ISC DHCPv4 server."""
        return self._get("dhcpv4/leases/searchLease")