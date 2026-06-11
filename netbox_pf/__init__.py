# SPDX-License-Identifier: AGPL-3.0-or-later
"""netbox-pf: a native NetBox source of truth for firewall rules + aliases on both
**OPNsense and pfSense** (FreeBSD pf).

Unlike netbox-security (Junos zones/policies) and netbox-acls (Cisco extended ACLs),
this models the exact pf schema, so either platform's ``<filter><rule>`` round-trips
with zero field loss and the ansible-tofu opnsense ``firewall_rules`` contract reads it
back 1:1. Platform-specific identifiers (pfSense ``tracker``, OPNsense ``uuid``) and the
long-tail pf options are preserved verbatim.
"""
from netbox.plugins import PluginConfig

__version__ = "0.1.1"


class NetBoxPFConfig(PluginConfig):
    name = "netbox_pf"
    verbose_name = "NetBox pf"
    description = "Native SoT for pf/OPNsense firewall rules and aliases"
    version = __version__
    author = "Jameson"
    base_url = "pf"
    min_version = "4.6.0"
    max_version = "4.6.99"


config = NetBoxPFConfig
