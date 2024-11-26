# PyOPN

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Auto Release](https://img.shields.io/badge/release-auto.svg?colorA=888888&colorB=9B065A&label=auto)](https://github.com/intuit/auto)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![tests](https://github.com/alexchristy/PyOPN/actions/workflows/tests.yml/badge.svg)](https://github.com/alexchristy/PyOPN/actions)
[![PyPI version](https://badge.fury.io/py/pyopn.svg)](https://badge.fury.io/py/pyopn)

A simple Python wrapper for the OPNsense REST API.

Forked from [mtrinish/pyopnsense](https://github.com/mtreinish/pyopnsense) and modeled after [proxmoxer/proxmoxer](https://github.com/proxmoxer/proxmoxer).

The purpose of this library is also to extend the existing [OPNsense API reference](https://docs.opnsense.org/development/api.html). Each endpoint that has been implemented in this library has a corresponding docstring with a brief explanation of what the endpoint does. Additionally, POST requests that require payloads include the corresponding JSON payloads that are required and other relevant information.

## Installation

```bash
pip install pyopn
```

## Usage

### Prerequisites

In order to access the OPNsense API you first need to [generate an API key](https://docs.opnsense.org/development/how-tos/api.html#creating-keys). 

### Example

```python
from pyopn import OPNsenseAPI

opn = OPNsenseAPI("https://192.168.199.1", api_key_file="OPNsense.localdomain_apikey.txt")

print(opn.kea.dhcpv4.search_reservation())
```

### Structure

The endpoints are organized as `opn.module.controller.command(param1, param2, data)`. Anytime camel case is used in the endpoint names, this wrapper uses snake case. 

Parameters are passed in as arguments and are positioned in the order of they appear in the [OPNsense API reference](https://docs.opnsense.org/development/api.html). If an endpoint accepts a JSON payload, the function will have a `data` arguement in the last position where you can pass in a Python dictionary.

**Ex:** `kea/dhcpv4/setSubnet` --> `opn.kea.dhcpv4.set_subnet(uuid, data)` ([Kea API Reference](https://docs.opnsense.org/development/api/core/kea.html))

## Implementation Checklist

Below is a checklist of core OPNsense API modules. Checked off modules are completed

- [ ] [Captiveportal](https://docs.opnsense.org/development/api/core/captiveportal.html)
- [ ] [Core](https://docs.opnsense.org/development/api/core/core.html)
- [ ] [Cron](https://docs.opnsense.org/development/api/core/cron.html)
- [ ] [Dhcp](https://docs.opnsense.org/development/api/core/dhcp.html)
- [X] [Dhcpv4](https://docs.opnsense.org/development/api/core/dhcpv4.html)
- [ ] [Dhcpv6](https://docs.opnsense.org/development/api/core/dhcpv6.html)
- [ ] [Dhcrelay](https://docs.opnsense.org/development/api/core/dhcrelay.html)
- [ ] [Diagnostics](https://docs.opnsense.org/development/api/core/diagnostics.html)
- [ ] [Firewall](https://docs.opnsense.org/development/api/core/firewall.html)
- [ ] [Firmware](https://docs.opnsense.org/development/api/core/firmware.html)
- [ ] [Ids](https://docs.opnsense.org/development/api/core/ids.html)
- [ ] [Interfaces](https://docs.opnsense.org/development/api/core/interfaces.html)
- [ ] [Ipsec](https://docs.opnsense.org/development/api/core/ipsec.html)
- [X] [Kea](https://docs.opnsense.org/development/api/core/kea.html)
- [ ] [Menu](https://docs.opnsense.org/development/api/core/menu.html)
- [ ] [Monit](https://docs.opnsense.org/development/api/core/monit.html)
- [ ] [Openvpn](https://docs.opnsense.org/development/api/core/openvpn.html)
- [ ] [Proxy](https://docs.opnsense.org/development/api/core/proxy.html)
- [ ] [Routes](https://docs.opnsense.org/development/api/core/routes.html)
- [ ] [Routing](https://docs.opnsense.org/development/api/core/routing.html)
- [ ] [Syslog](https://docs.opnsense.org/development/api/core/syslog.html)
- [ ] [Trafficshaper](https://docs.opnsense.org/development/api/core/trafficshaper.html)
- [ ] [Trust](https://docs.opnsense.org/development/api/core/trust.html)
- [ ] [Unbound](https://docs.opnsense.org/development/api/core/unbound.html)
- [ ] [Wireguard](https://docs.opnsense.org/development/api/core/wireguard.html)

## Contributing

Feel free to contribute to the library if there are missing endpoints you need. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and a quick tutorial on how to add new endpoints.

## License

This project is licensed under the [GPL-3.0 license](LICENSE) - see the [LICENSE](LICENSE) file for details

## Acknowledgments

  - [mtreinish](https://github.com/mtreinish) for original code base this project was forked from
  - [proxmoxer](https://github.com/proxmoxer/proxmoxer) for the design pattern
