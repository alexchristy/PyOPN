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

from typing import Any, Optional

from pyopn import client


class CtrlAgentClient(client.OPNClient):
    """A client for interacting with the kea/ctrl_agent endpoints.

    :param str api_key: The API key to use for requests
    :param str api_secret: The API secret to use for requests
    :param str base_url: The base API endpoint for the OPNsense deployment
    """

    def get(self) -> dict[str, Any]:
        """Get the Kea controller agent configuration.

        :return: API response
        :rtype: dict[str, Any]
        """
        return self._get("kea/ctrl_agent/get", raw=False)

    def set(self, data: dict[str, Any]) -> dict[str, Any]:
        """Configure the Kea control agent.

        **Note:** Make sure to POST to the `kea/service/reconfigure` endpoint after this
        to enable changes.

        This function uses the `KeaCtrlAgent.xml` data model. For details, see:
        https://github.com/opnsense/core/blob/master/src/opnsense/mvc/app/models/OPNsense/Kea/KeaCtrlAgent.xml

        :param dict data: Python dictionary to be used for the body of the request.
            The dictionary should follow the `KeaCtrlAgent.xml` data model.

        Example:
            ```python
            # Enable Control Agent with default configuration
            data = {
                "ctrlagent": {
                    "general": {
                        "enabled":"1",
                        "http_host":"127.0.0.1",
                        "http_port":"8000"
                    }
                }
            }
            ```

        :return: API response
        :rtype: dict[str, Any]

        """
        return self._post("kea/ctrl_agent/set", data, raw=False)


class Dhcpv4Client(client.OPNClient):
    """A client for interacting with the kea/dhcpv4 endpoints.

    :param str api_key: The API key to use for requests
    :param str api_secret: The API secret to use for requests
    :param str base_url: The base API endpoint for the OPNsense deployment
    """

    def get(self) -> dict[str, Any]:
        """Get the Kea DHCPv4 server configuration.

        :return: API response
        :rtype: dict[str, Any]
        """
        return self._get("kea/dhcpv4/get", raw=False)

    def set(self, data: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """Set configuration for the Kea DHCPv4 server.

        :param dict data: Python dictionary to be used for the body of the request.

            **Note on applying settings:** By default the OPNsense GUI will post the below
            data when you click the 'Apply' button after setting any DHCPv4 server settings.
            However, manually testing with an empty dictionary works for applying settings.

        Example:
            ```python
            data = {
                "dhcpv4": {
                    "general": {
                    "enabled": "0",
                    "interfaces": "",
                    "valid_lifetime": "4000",
                    "fwrules": "1"
                    },
                    "ha": {
                    "enabled": "0",
                    "this_server_name": "",
                    "max_unacked_clients": "2"
                    }
                }
            }
            ```

        :return: API response
        :rtype: dict[str, Any]

        """
        if not data:
            data = {}
        return self._post("kea/dhcpv4/set", data, raw=False)

    def add_subnet(self, data: dict[str, Any]) -> dict[str, Any]:
        r"""Add subnet to the Kea DHCPv4 server.

        **Note:** Make sure to POST to the `kea/dhcpv4/set` and then `kea/service/reconfigure` endpoints after this
        to enable changes.

        This function uses the `KeaDhcpv4.xml` data model. For details, see:
        https://github.com/opnsense/core/blob/master/src/opnsense/mvc/app/models/OPNsense/Kea/KeaDhcpv4.xml

        :param dict data: Python dictionary to be used for the body of the request.
            The dictionary should follow the `KeaDhcpv4.xml` data model.

        Example:
            ```python
            data = {
                "subnet4": {
                    "subnet": "192.168.199.0/24",
                    "description": "Full network subnet",
                    "pools": "192.168.199.10 - 192.168.199.15\\n192.168.199.64/28",
                    "option_data_autocollect": "1",
                    "option_data": {
                        "routers": "",
                        "static_routes": "",
                        "domain_name_servers": "",
                        "domain_name": "",
                        "domain_search": "",
                        "ntp_servers": "",
                        "time_servers": "",
                        "tftp_server_name": "",
                        "boot_file_name": ""
                    },
                    "next_server": ""
                }
            }
            ```

        :return: API response
        :rtype: dict[str, Any]

        """
        return self._post("kea/dhcpv4/addSubnet", data, raw=False)

    def del_subnet(self, uuid: str) -> dict[str, Any]:
        """Delete the subnet configuration on the Kea DHCPv4 server by UUID.

        **Note:** Make sure to POST to the `kea/service/reconfigure` endpoint after this
        to enable changes.

        :param str uuid: The UUID of the subnet to delete.

        :return: API response
        :rtype: dict[str, Any]
        """
        return self._post(f"kea/dhcpv4/delSubnet/{uuid}", {}, raw=False)

    def get_subnet(self, uuid: str) -> dict[str, Any]:
        """Get the configuration of a subnet on the Kea DHCPv4 server.

        :param str uuid: The UUID of the subnet to get the configuration for.

        :return: API response
        :rtype: dict[str, Any]
        """
        return self._get(f"kea/dhcpv4/getSubnet/{uuid}", raw=False)

    def search_subnet(self) -> dict[str, Any]:
        """Get the configured subnets for the Kea DHCPv4 server.

        :return: API response
        :rtype: dict[str, Any]
        """
        return self._get("kea/dhcpv4/searchSubnet", raw=False)

    def set_subnet(self, uuid: str, data: dict[str, Any]) -> dict[str, Any]:
        r"""Set subnet configuration on the Kea DHCPv4 server.

        **Note:** Make sure to POST to the `kea/dhcpv4/set` and then `kea/service/reconfigure` endpoints after this
        to apply changes.

        This function uses the `KeaDhcpv4.xml` data model. For details, see:
        https://github.com/opnsense/core/blob/master/src/opnsense/mvc/app/models/OPNsense/Kea/KeaDhcpv4.xml

        :param str uuid: The UUID of the subnet to set the configuration for.
        :param dict data: Python dictionary to be used for the body of the request.
            The dictionary should follow the `KeaDhcpv4.xml` data model.

        Example:
            ```python
            data = {
                "subnet4": {
                    "subnet": "192.168.199.0/24",
                    "description": "Full network subnet",
                    "pools": "192.168.199.10 - 192.168.199.15\\n192.168.199.64/28",
                    "option_data_autocollect": "1",
                    "option_data": {
                        "routers": "",
                        "static_routes": "",
                        "domain_name_servers": "",
                        "domain_name": "",
                        "domain_search": "",
                        "ntp_servers": "",
                        "time_servers": "",
                        "tftp_server_name": "",
                        "boot_file_name": ""
                    },
                    "next_server": ""
                }
            }
            ```

        :return: API response
        :rtype: dict[str, Any]

        """
        return self._post(f"kea/dhcpv4/setSubnet/{uuid}", data, raw=False)

    def search_reservation(self) -> dict[str, Any]:
        """Get the configured reservations on the Kea DHCPv4 server.

        :return: API response
        :rtype: dict[str, Any]
        """
        return self._get("kea/dhcpv4/searchReservation", raw=False)

    def add_reservation(self, data: dict[str, Any]) -> dict[str, Any]:
        """Add reservation to the Kea DHCPv4 server.

        **Note:** Make sure to POST to the `kea/dhcpv4/set` and then `kea/service/reconfigure` endpoints after this
        to enable changes.

        This function uses the `KeaDhcpv4.xml` data model. For details, see:
        https://github.com/opnsense/core/blob/master/src/opnsense/mvc/app/models/OPNsense/Kea/KeaDhcpv4.xml

        :param dict data: Python dictionary to be used for the body of the request.

        Example:
            ```python
            data = {
                "reservation": {
                    "description": "Reservation description here",
                    "hostname": "test.local",
                    "hw_address": "02:42:46:e2:c3:ac",
                    "ip_address": "192.168.199.200",
                    "subnet": "f0e59e66-194c-4a61-b6ee-e8e67c545788"
                }
            }
            ```

        :return: API response
        :rtype: dict[str, Any]

        """
        return self._post("kea/dhcpv4/addReservation", data, raw=False)

    def del_reservation(self, uuid: str) -> dict[str, Any]:
        """Delete reservation but UUID on the Kea DHCPv4 server.

        **Note:** Make sure to POST to the `kea/service/reconfigure` endpoint after this
        to enable changes.

        :param str uuid: UUID of the DHCP reservation to delete.

        :return: API response
        :rtype: dict[str, Any]
        """
        return self._post(f"kea/dhcpv4/delReservation/{uuid}", {}, raw=False)

    def download_reservations(self) -> str:
        """Download CSV of reservations on the Kea DHCPv4 server.

        :return: CSV-formatted string containing all DHCPv4 reservations configured on the Kea DHCPv4 server.
        :rtype: str
        """
        return self._get("kea/dhcpv4/downloadReservations", raw=True)

    def get_reservation(self, uuid: str) -> dict[str, Any]:
        """Get configuration of the reservation on Kea DHCPv4 server by UUID.

        :param str uuid: The UUID of the DHCP reservation to get the configuration for.

        :return: API response
        :rtype: dict[str, Any]
        """
        return self._get(f"kea/dhcpv4/getReservation/{uuid}", raw=False)

    def set_reservation(self, uuid: str, data: dict[str, Any]) -> dict[str, Any]:
        """Set DHCP reservation configuration on the Kea DHCPv4 server.

        **Note:** Make sure to POST to the `kea/dhcpv4/set` and then `kea/service/reconfigure` endpoints after this
        to enable changes.

        This function uses the `KeaDhcpv4.xml` data model. For details, see:
        https://github.com/opnsense/core/blob/master/src/opnsense/mvc/app/models/OPNsense/Kea/KeaDhcpv4.xml

        :param str uuid: The UUID of the reservation to set the configuration for.
        :param dict data: Python dictionary to be used for the body of the request.

        Example:
            ```python
            data = {
                "reservation": {
                    "description": "Reservation description here",
                    "hostname": "test.local",
                    "hw_address": "02:42:46:e2:c3:ac",
                    "ip_address": "192.168.199.200",
                    "subnet": "f0e59e66-194c-4a61-b6ee-e8e67c545788"
                }
            }
            ```

        :return: API response
        :rtype: dict[str, Any]

        """
        return self._post(f"kea/dhcpv4/setReservation/{uuid}", data, raw=False)

    def upload_reservations(
        self, file_path: Optional[str] = None, data: Optional[str] = None
    ) -> dict[str, Any]:
        """Upload a CSV of DHCP reservations to the Kea DHCPv4 server.

        **Note:** Make sure to POST to the `kea/dhcpv4/set` and then `kea/service/reconfigure` endpoints after this
        to enable changes.

        :param file_path: Path to the CSV file to upload. Mutually exclusive with `data`.
        :param data: Raw CSV data as a string. Mutually exclusive with `file_path`.

            Example CSV:
            ```csv
            ip_address,hw_address,hostname,description
            192.168.199.69,02:42:46:e2:c3:a6,blah.local,"VMID Blah"
            ```

        :return: API response
        :rtype: dict[str, Any]

        :raises ValueError: If both or neither of `file_path` and `data` are provided.
        """
        if file_path and data:
            msg = "Provide either `file_path` or `data`, but not both."
            raise ValueError(msg)
        if not file_path and not data:
            msg = "You must provide either `file_path` or `data`."
            raise ValueError(msg)

        if file_path:
            return self._post_file(
                "kea/dhcpv4/uploadReservations", file_path, raw=False
            )
        if data:
            return self._post_csv_data("kea/dhcpv4/uploadReservations", data, raw=False)
        return {"error": "No file path or data provided."}

    def search_peer(self) -> dict[str, Any]:
        """Get the configured peers for the Kea DHCPv4 server.

        :return: API response
        :rtype: dict[str, Any]
        """
        return self._get("kea/dhcpv4/searchPeer", raw=False)

    def get_peer(self, uuid: str) -> dict[str, Any]:
        """Get the configuration for a peer on the Kea DHCPv4 server by UUID.

        :param str uuid: The UUID of the peer to get the configuration for.

        :return: API response
        :rtype: dict[str, Any]
        """
        return self._get(f"kea/dhcpv4/getPeer/{uuid}", raw=False)

    def del_peer(self, uuid: str) -> dict[str, Any]:
        """Delete the peer on the Kea DHCPv4 server by UUID.

        **Note:** Make sure to POST to the `kea/service/reconfigure` endpoint after this
        to enable changes.

        :param str uuid: The UUID of the peer to delete.

        :return: API response
        :rtype: dict[str, Any]
        """
        return self._post(f"kea/dhcpv4/delPeer/{uuid}", {}, raw=False)

    def add_peer(self, data: dict[str, Any]) -> dict[str, Any]:
        """Add peer to the Kea DHCPv4 server.

        **Note:** Make sure to POST to the `kea/dhcpv4/set` and then `kea/service/reconfigure` endpoints after this
        to enable changes.

        This function uses the `KeaDhcpv4.xml` data model. For details, see:
        https://github.com/opnsense/core/blob/master/src/opnsense/mvc/app/models/OPNsense/Kea/KeaDhcpv4.xml

        :param dict data: Python dictionary to be used for the body of the request.

        Example:
            ```python
            data = {
                "peer": {
                    "name": "Test peer",
                    "role": "primary", # primary or standby
                    "url": "http://192.168.199.252:8001/"
                }
            }
            ```

        :return: API response
        :rtype: dict[str, Any]

        """
        return self._post("kea/dhcpv4/addPeer", data, raw=False)

    def set_peer(self, uuid: str, data: dict[str, Any]) -> dict[str, Any]:
        """Set configuration of peer on the Kea DHCPv4 server by UUID.

        **Note:** Make sure to POST to the `kea/dhcpv4/set` and then `kea/service/reconfigure` endpoints after this
        to enable changes.

        This function uses the `KeaDhcpv4.xml` data model. For details, see:
        https://github.com/opnsense/core/blob/master/src/opnsense/mvc/app/models/OPNsense/Kea/KeaDhcpv4.xml

        :param str uuid: The UUID of the peer to set the configuration for.
        :param dict data: Python dictionary to be used for the body of the request.

        Example:
            ```python
            data = {
                "peer": {
                    "name": "Test peer",
                    "role": "primary", # primary or standby
                    "url": "http://192.168.199.252:8001/"
                }
            }
            ```

        :return: API response
        :rtype: dict[str, Any]

        """
        return self._post(f"kea/dhcpv4/setPeer/{uuid}", data, raw=False)


class Leases4Client(client.OPNClient):
    """A client for interacting with the kea/leases4 endpoint.

    :param str api_key: The API key to use for requests
    :param str api_secret: The API secret to use for requests
    :param str base_url: The base API endpoint for the OPNsense deployment
    """

    def search(self) -> dict[str, Any]:
        """Get all active leases on the Kea DHCPv4 server.

        :return: API response
        :rtype: dict[str, Any]
        """
        return self._get("kea/leases4/search", raw=False)


class ServiceClient(client.OPNClient):
    """A client for interacting with the kea/service endpoint.

    :param str api_key: The API key to use for requests
    :param str api_secret: The API secret to use for requests
    :param str base_url: The base API endpoint for the OPNsense deployment
    """

    def reconfigure(self) -> dict[str, Any]:
        """Enable/Reconfigure the Kea DHCP service with the currently set configuration.

        :return: API response
        :rtype: dict[str, Any]
        """
        return self._post("kea/service/reconfigure", {}, raw=False)

    def status(self) -> dict[str, Any]:
        """Get the status of the Kea DHCP service.

        :return: API response
        :rtype: dict[str, Any]
        """
        return self._get("kea/service/status", raw=False)
