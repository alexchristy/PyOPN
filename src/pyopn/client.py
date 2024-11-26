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
from typing import Any, Literal, Union, overload

import requests
import urllib3

from pyopn import exceptions
from pyopn.constants import DEFAULT_TIMEOUT, HTTP_SUCCESS


class OPNClient(object):
    """Representation of the OPNsense API client."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str,
        verify_cert: bool = False,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        """Initialize the OPNsense API client."""
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.verify_cert = verify_cert
        if not self.verify_cert:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.timeout = timeout

    def _process_response(
        self, response: requests.Response, raw: bool
    ) -> Union[str, dict[str, Any]]:
        """Return data from response objects.

        :param Response response: Response object to process.
        :param bool raw: If True, return the raw text response as a string.
                    If False, return the JSON response parsed as a dictionary.

        :return: A string containing the raw text response if `raw` is `True`. A dictionary of the JSON response if `raw` is `False`.
        :rtype: Union[str, dict[str, Any]]
        """
        if response.status_code in HTTP_SUCCESS:
            return str(response.text) if raw else json.loads(response.text)
        raise exceptions.APIError(
            status_code=response.status_code, resp_body=response.text
        )

    @overload
    def _get(self, endpoint: str, raw: Literal[True]) -> str: ...

    @overload
    def _get(self, endpoint: str, raw: Literal[False]) -> dict[str, Any]: ...

    def _get(self, endpoint: str, raw: bool) -> Union[str, dict[str, Any]]:
        """Send GET request to the specified endpoint.

        :param str endpoint: API endpoint to send the request to.
        :param bool raw: If True, return the raw text response as a string.
                    If False, return the JSON response parsed as a dictionary.

        :return: A string containing the raw text response if `raw` is `True`. A dictionary of the JSON response if `raw` is `False`.
        :rtype: Union[str, dict[str, Any]]
        """
        req_url = "{}/{}".format(self.base_url, endpoint)
        response = requests.get(
            req_url,
            verify=self.verify_cert,
            auth=(self.api_key, self.api_secret),
            timeout=self.timeout,
        )
        return self._process_response(response, raw)

    @overload
    def _post(self, endpoint: str, data: dict[str, Any], raw: Literal[True]) -> str: ...

    @overload
    def _post(
        self, endpoint: str, data: dict[str, Any], raw: Literal[False]
    ) -> dict[str, Any]: ...

    def _post(
        self, endpoint: str, data: dict[str, Any], raw: bool
    ) -> Union[str, dict[str, Any]]:
        """Send POST request to the specified endpoint with a JSON payload.

        :param str endpoint: API endpoint to send the request to.
        :param dict[str, Any] data: Dictionary to send as JSON body.
        :param bool raw: If True, return the raw text response as a string.
                    If False, return the JSON response parsed as a dictionary.

        :return: A string containing the raw text response if `raw` is `True`. A dictionary of the JSON response if `raw` is `False`.
        :rtype: Union[str, dict[str, Any]]
        """
        req_url = "{}/{}".format(self.base_url, endpoint)
        response = requests.post(
            req_url,
            json=data,
            verify=self.verify_cert,
            auth=(self.api_key, self.api_secret),
            timeout=self.timeout,
        )
        return self._process_response(response, raw)

    @overload
    def _post_file(self, endpoint: str, file_path: str, raw: Literal[True]) -> str: ...

    @overload
    def _post_file(
        self, endpoint: str, file_path: str, raw: Literal[False]
    ) -> dict[str, Any]: ...

    def _post_file(
        self, endpoint: str, file_path: str, raw: bool
    ) -> Union[str, dict[str, Any]]:
        """Upload a file to the specified endpoint as JSON payload.

        :param str endpoint: API endpoint to send the request to.
        :param str file_path: Path of file to upload.
        :param bool raw: If True, return the raw text response as a string.
                    If False, return the JSON response parsed as a dictionary.

        :return: A string containing the raw text response if `raw` is `True`. A dictionary of the JSON response if `raw` is `False`.
        :rtype: Union[str, dict[str, Any]]
        """
        req_url = f"{self.base_url}/{endpoint}"

        # Read the file content
        with open(file_path, "r") as f:
            file_content = f.read()

        # Prepare the JSON payload
        payload = {"payload": file_content, "filename": file_path.split("/")[-1]}

        response = requests.post(
            req_url,
            json=payload,  # Send as JSON
            verify=self.verify_cert,
            auth=(self.api_key, self.api_secret),
            timeout=self.timeout,
        )
        return self._process_response(response, raw)

    @overload
    def _post_csv_data(
        self, endpoint: str, csv_data: str, raw: Literal[True]
    ) -> str: ...

    @overload
    def _post_csv_data(
        self, endpoint: str, csv_data: str, raw: Literal[False]
    ) -> dict[str, Any]: ...

    def _post_csv_data(
        self, endpoint: str, csv_data: str, raw: bool
    ) -> Union[str, dict[str, Any]]:
        """Upload CSV data to the specified endpoint as JSON payload.

        :param str endpoint: API endpoint to send the request to.
        :param str csv_data: CSV data as a string.
        :param bool raw: If True, return the raw text response as a string.
                    If False, return the JSON response parsed as a dictionary.

        :return: A string containing the raw text response if `raw` is `True`. A dictionary of the JSON response if `raw` is `False`.
        :rtype: Union[str, dict[str, Any]]
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
