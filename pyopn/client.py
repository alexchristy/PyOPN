# Copyright 2018 Matthew Treinish
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


import json

import requests

from pyopn import exceptions
from requests.packages import urllib3
from pyopn.constants import DEFAULT_TIMEOUT, HTTP_SUCCESS


class OPNClient(object):
    """Representation of the OPNsense API client."""

    def __init__(
        self, api_key, api_secret, base_url, verify_cert=False, timeout=DEFAULT_TIMEOUT
    ):
        """Initialize the OPNsense API client."""
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.verify_cert = verify_cert
        if self.verify_cert == False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.timeout = timeout

    def _process_response(self, response, raw=False):
        """Handle the response."""
        if response.status_code in HTTP_SUCCESS:
            return response.text if raw else json.loads(response.text)
        else:
            raise exceptions.APIException(
                status_code=response.status_code, resp_body=response.text
            )

    def _get(self, endpoint, raw=False):
        req_url = "{}/{}".format(self.base_url, endpoint)
        response = requests.get(
            req_url,
            verify=self.verify_cert,
            auth=(self.api_key, self.api_secret),
            timeout=self.timeout,
        )
        return self._process_response(response, raw)

    def _post(self, endpoint, data, raw=False):
        req_url = "{}/{}".format(self.base_url, endpoint)
        response = requests.post(
            req_url,
            json=data,
            verify=self.verify_cert,
            auth=(self.api_key, self.api_secret),
            timeout=self.timeout,
        )
        return self._process_response(response, raw)

    def _post_file(self, endpoint: str, file_path: str, raw=False):
        """Upload a file to the specified endpoint as JSON payload.

        :param endpoint: API endpoint to send the request to.
        :param file_path: Path to the file to be uploaded.
        :param raw: Return raw text response if True.
        :return: API response
        """
        req_url = f"{self.base_url}/{endpoint}"

        # Read the file content
        with open(file_path, "r") as f:
            csv_content = f.read()

        # Prepare the JSON payload
        payload = {"payload": csv_content, "filename": file_path.split("/")[-1]}

        response = requests.post(
            req_url,
            json=payload,  # Send as JSON
            verify=self.verify_cert,
            auth=(self.api_key, self.api_secret),
            timeout=self.timeout,
        )
        return self._process_response(response, raw)

    def _post_csv_data(self, endpoint: str, csv_data: str, raw=False):
        """Upload raw CSV data to the specified endpoint as JSON payload.

        :param endpoint: API endpoint to send the request to.
        :param csv_data: Raw CSV data as a string.
        :param raw: Return raw text response if True.
        :return: API response
        """
        req_url = f"{self.base_url}/{endpoint}"

        # Prepare the JSON payload
        payload = {
            "payload": csv_data,
            "filename": "data.csv",  # Default filename for the uploaded data
        }

        # Send the request
        response = requests.post(
            req_url,
            json=payload,  # Send as JSON
            verify=self.verify_cert,
            auth=(self.api_key, self.api_secret),
            timeout=self.timeout,
        )
        return self._process_response(response, raw)
