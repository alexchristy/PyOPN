# Copyright 2024 Alex Christy
#
# This file is part of pyopnsense
#
# pyopnsense is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyopnsense is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyopnsense. If not, see <http://www.gnu.org/licenses/>.

from pyopnsense import client
from pyopnsense.base_namespace import BaseNamespace

class Dhcpv4Namespace(BaseNamespace):
    """Namespace for Dhcpv4-related API clients."""

    @property
    def service(self):
        return self._initialize_client("service", ServiceClient)



class ServiceClient(client.OPNClient):
    """A client for interacting with the dhcpv4/service endpoint.

    :param str api_key: The API key to use for requests
    :param str api_secret: The API secret to use for requests
    :param str base_url: The base API endpoint for the OPNsense deployment
    """

    def status(self):
        """Return the current netflow status.

        :returns: A dict representing the current status of netflow
        :rtype: dict
        """
        return self._get("dhcpv4/service/status")