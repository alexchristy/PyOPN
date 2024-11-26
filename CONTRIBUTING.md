# Contributing

Pull requests, bug reports, and all other forms of contribution are welcomed and highly encouraged! :octocat: 

***Note:** Make sure to make a PR against this repository and not the originally forked repository*

## Enviroment Setup

1) Download repo

    ```bash
    git clone https://github.com/alexchristy/PyOPN
    ```

2) Enter repo

    ```bash
    cd pyopn
    ```

3) Create virtual enviroment

    ```bash
    python3 -m venv venv

    # Activate virtual environment
    source venv/bin/activate
    ```

4) Install dependencies

    ```bash
    pip install -r requirements.txt
    pip install -r dev-requirements.txt
    ```

5) All done!

    * See the sections below on how to add new endpoints to the library.

## Project Stucture

```txt
PyOPN
├── pyopn/
|   ├── tests/
|   ├── api.py
|   ├── core/
|       ├── module_name.py
|       ├── module_name_namespace.py
```

### Key Files

* `tests/` - Folder will all the tests for the project.
* `api.py` - Frontend of the API wrapper.
* `core/` - Folder with all the endpoints associated with the [Core API](https://docs.opnsense.org/development/api.html#core-api).
    * `module_name.py` - Library implementation of the endpoints associated with one of the OPNsense API modules. The API module's controllers are grouped by controller where each command is a method of the corresponding controller class.
    * `module_name_namespace.py` - The namespace coresponding to a implemented API module. Makes the endpoints accessible through the `OPNsenseAPI` object.

## Code Style

Since this API is a very basic wrapper of the API, one of the main functions of this library is to extend the official API documentation. This is mainly done through the docstrings of the functions that implmenent the API endpoints.

The majority of the contributed code in this project should be the docstrings as the core request functionality is already implemented.

### Precommit Hooks

This project uses the [Black](https://github.com/psf/black) formatting tool and the [Ruff](https://github.com/astral-sh/ruff) linter. Ensure that your code passes the following:
- `ruff check --fix` - Runs linting rules.
- `ruff format` - Runs linter formatting rules.
- `black .` - Formats code to black standards (Run from root of repository).
- `mypy src/` - Runs type checking against all source files.
- `pytest` - Run all tests.

These are configured in the `.pre-commit-config.yaml` and commits will fail unless all commands pass.

### Docstring Format

1) Single sentence endpoint decription.
2) Any critical notes for using the endpoint. Prefix with `**Notes:**`. For example, some endpoints require calling other endpoints to applying the changes.
3) Less critical notes. Usually references to data models used by endpoints.
4) List of parameters with data types and descriptions.
5) If a **data** paramter is included:
    * It's data type will always be: `dict[str, Any]`
    * Always the last parameter of the function
    * Should include an example of the payload required tabbed under the data paramter in the docstring.
6) Return type of the function.
    * If the endpoint returns JSON, the return type is: `dict[str, Any]`

### Endpoint Example

*For a file-related endpoint example see `upload_reservations` in `pyopn/core/kea.py`*

```python
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
```

## Adding a New Endpoint

*This tutorial will show how to implement the `Kea` module and create the `kea/ctrl_agent/get` endpoint ([OPNsense Kea API docs](https://docs.opnsense.org/development/api/core/kea.html)).*

1) Become acquainted with the [Official OPNsense API docs](https://docs.opnsense.org/development/api.html).
2) Create the module files in `pyopn/core/`
    * Module file: `module_name.py`
    * Module namespace file: `module_name_namespace.py`
3) In `module_name.py`:
    * Create a class for each of the API module controllers that inherits from `client.OPNClient`. 
        * Format: `{PascalCaseControllerName}Client`
    * Add a docstring with a description of the controller and the inherited parameters.
    * Add endpoints as class methods.
    * **Full Example:** (For the `ctrl_agent` controller that is part of the `Kea` module in `pyopn/core/kea.py`)

        ```python
        from pyopn import client

        class CtrlAgentClient(client.OPNClient):
            """A client for interacting with the kea/ctrl_agent endpoints.

            :param str api_key: The API key to use for requests
            :param str api_secret: The API secret to use for requests
            :param str base_url: The base API endpoint for the OPNsense  deployment
            """

            def get(self) -> dict[str, Any]:
                """Get the Kea controller agent configuration.
                
                :return: API response
                :rtype: dict[str, Any]
                """
                return self._get("kea/ctrl_agent/get", raw=False)
        ```
4) In `module_name_namespace.py`:
    * Import all of the API controller classes from `module_name.py`
    * Create a class for the API module namespace that inherits from `BaseNamespace`. 
        * Format: `{PascalCaseModuleName}Namespace`
        * Add a simple docstring
    * Create an attribute for each controller class you import.
        * Format: `_controller_name: Optional[ControllerNameClient] = None`
    * Add the corresponding property
        * Format: (see `@property` functions in Full Example below)
    * **Full Example:** (For the `Kea` module in `pyopn/core/kea_namespace.py`)
        ```python
        from typing import Optional
        from pyopn.base_namespace import BaseNamespace

        # Import the client class
        from pyopn.core.kea import (
            CtrlAgentClient
        )

        class KeaNamespace(BaseNamespace):
            """Namespace for Kea related API clients."""

            # Internal attribute for lazy initialization
            _ctrl_agent: Optional[CtrlAgentClient] = None
            (...)

            @property
            def ctrl_agent(self) -> CtrlAgentClient:
                if not self._ctrl_agent:
                    self._ctrl_agent = self._initialize_client("ctrl_agent", CtrlAgentClient)
                return cast(CtrlAgentClient, self._ctrl_agent)
            
        ```
5) In `pyopn/api.py`:
    * Import the API module namespace
    * Add the corresponding property in the `OPNsenseAPI` class (see Full Example below)
    * **Full Example:** (For the `Kea` module in `pyopn/api.py`)
        ```python
        from pyopn.core.kea_namespace import KeaNamespace

        class OPNsenseAPI(object):
            (...)

            @property
            def kea(self) -> KeaNamespace:
                if "kea" not in self._namespaces:
                    self._namespaces["kea"] = KeaNamespace(self)
                return cast(KeaNamespace, self._namespaces["kea"])
        ```

## No semver label!

![image](https://github.com/user-attachments/assets/1558ccd3-ede2-4963-aa37-5ccfd9ce3c58)

If you recieve the above error it means that you did not attach a semantic (sem) version (ver) label to your PR.

### Adding a Semantic Version Label

1) Click the gear icon by `Labels` on the right hand side of your PR.

    ![image](https://github.com/user-attachments/assets/4a1b0227-4f53-4339-bdcd-91e8e37cc31f)

2) Choose between the labels: `major`, `minor`, and `patch`. If you are unsure which one to choose, see the summary section at the top of the page of this [semantic versioning guide](https://semver.org/).

    ![image](https://github.com/user-attachments/assets/a03f33b4-1f76-4f00-942b-51f8be78f16b)

3) As soon as you add the label, it will kick off the check once again which should pass.

