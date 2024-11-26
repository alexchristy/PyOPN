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
from unittest import mock

from pyopn import client, exceptions
from pyopn.tests import base


class TestOPNClient(base.TestCase):
    """Clas for testning the OPNClient class methods."""

    @mock.patch("requests.get")
    def test_get_success(self, request_mock: mock.MagicMock) -> None:
        """Test a successful GET request."""
        response_mock = mock.MagicMock()
        response_mock.status_code = 200
        response_mock.text = json.dumps({"a": "body"})
        request_mock.return_value = response_mock
        opnclient = client.OPNClient("", "", "", timeout=10)
        resp = opnclient._get("fake_url", raw=False)
        self.assertEqual({"a": "body"}, resp)
        request_mock.assert_called_once_with(
            "/fake_url", auth=("", ""), timeout=10, verify=False
        )

    @mock.patch("requests.get")
    def test_get_failures(self, request_mock: mock.MagicMock) -> None:
        """Test a failed GET request."""
        response_mock = mock.MagicMock()
        response_mock.status_code = 401
        response_mock.text = json.dumps({"a": "body"})
        request_mock.return_value = response_mock
        opnclient = client.OPNClient("", "", "")
        self.assertRaises(exceptions.APIError, opnclient._get, "fake_url", raw=False)
        request_mock.assert_called_once_with(
            "/fake_url", auth=("", ""), timeout=5, verify=False
        )

    @mock.patch("requests.post")
    def test_post_success(self, request_mock: mock.MagicMock) -> None:
        """Test a successful POST request with a body."""
        response_mock = mock.MagicMock()
        response_mock.status_code = 200
        response_mock.text = json.dumps({"a": "body"})
        request_mock.return_value = response_mock
        opnclient = client.OPNClient("", "", "")
        resp = opnclient._post("fake_url", {}, raw=False)
        self.assertEqual({"a": "body"}, resp)
        request_mock.assert_called_once_with(
            "/fake_url", json={}, auth=("", ""), timeout=5, verify=False
        )

    @mock.patch("requests.post")
    def test_post_failures(self, request_mock: mock.MagicMock) -> None:
        """Test a failed POST request with a body."""
        response_mock = mock.MagicMock()
        response_mock.status_code = 401
        response_mock.text = json.dumps({"a": "body"})
        request_mock.return_value = response_mock
        opnclient = client.OPNClient("", "", "")
        self.assertRaises(
            exceptions.APIError, opnclient._post, "fake_url", {}, raw=False
        )
        request_mock.assert_called_once_with(
            "/fake_url", json={}, auth=("", ""), timeout=5, verify=False
        )

    # Test for _post_file method
    @mock.patch("requests.post")
    def test_post_file_success(self, request_mock: mock.MagicMock) -> None:
        """Test a successful file POST request."""
        response_mock = mock.MagicMock()
        response_mock.status_code = 200
        response_mock.text = json.dumps({"status": "success"})
        request_mock.return_value = response_mock

        # Create client instance
        opnclient = client.OPNClient("", "", "")

        # Mock open to simulate file content
        with mock.patch("builtins.open", mock.mock_open(read_data="file content")):
            resp = opnclient._post_file("fake_url", "path/to/file.csv", raw=False)
            self.assertEqual({"status": "success"}, resp)

        # Check that the correct arguments were passed to requests.post
        request_mock.assert_called_once_with(
            "/fake_url",
            json={"payload": "file content", "filename": "file.csv"},
            auth=("", ""),
            timeout=5,
            verify=False,
        )

    @mock.patch("requests.post")
    def test_post_file_failure(self, request_mock: mock.MagicMock) -> None:
        """Test a failed file POST request."""
        response_mock = mock.MagicMock()
        response_mock.status_code = 400
        response_mock.text = json.dumps({"error": "bad request"})
        request_mock.return_value = response_mock

        opnclient = client.OPNClient("", "", "")

        with mock.patch("builtins.open", mock.mock_open(read_data="file content")):
            self.assertRaises(
                exceptions.APIError,
                opnclient._post_file,
                "fake_url",
                "path/to/file.csv",
                raw=False,
            )

        request_mock.assert_called_once_with(
            "/fake_url",
            json={"payload": "file content", "filename": "file.csv"},
            auth=("", ""),
            timeout=5,
            verify=False,
        )

    # Test for _post_csv_data method
    @mock.patch("requests.post")
    def test_post_csv_data_success(self, request_mock: mock.MagicMock) -> None:
        """Test a successful CSV data POST request."""
        response_mock = mock.MagicMock()
        response_mock.status_code = 200
        response_mock.text = json.dumps({"status": "success"})
        request_mock.return_value = response_mock

        opnclient = client.OPNClient("", "", "")
        csv_data = "id,name\n1,John Doe\n2,Jane Doe"
        resp = opnclient._post_csv_data("fake_url", csv_data, raw=False)
        self.assertEqual({"status": "success"}, resp)

        request_mock.assert_called_once_with(
            "/fake_url",
            json={"payload": csv_data, "filename": "data.csv"},
            auth=("", ""),
            timeout=5,
            verify=False,
        )

    @mock.patch("requests.post")
    def test_post_csv_data_failure(self, request_mock: mock.MagicMock) -> None:
        """Test a failed CSV data POST request."""
        response_mock = mock.MagicMock()
        response_mock.status_code = 500
        response_mock.text = json.dumps({"error": "internal server error"})
        request_mock.return_value = response_mock

        opnclient = client.OPNClient("", "", "")
        csv_data = "id,name\n1,John Doe\n2,Jane Doe"
        self.assertRaises(
            exceptions.APIError,
            opnclient._post_csv_data,
            "fake_url",
            csv_data,
            raw=False,
        )

        request_mock.assert_called_once_with(
            "/fake_url",
            json={"payload": csv_data, "filename": "data.csv"},
            auth=("", ""),
            timeout=5,
            verify=False,
        )
