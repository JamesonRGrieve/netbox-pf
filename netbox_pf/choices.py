# SPDX-License-Identifier: AGPL-3.0-or-later
"""Choice sets for the pf model. Values match OPNsense/pf config.xml tokens verbatim."""
from utilities.choices import ChoiceSet


class FirewallActionChoices(ChoiceSet):
    PASS = "pass"
    BLOCK = "block"
    REJECT = "reject"
    CHOICES = [(PASS, "Pass", "green"), (BLOCK, "Block", "red"), (REJECT, "Reject", "orange")]


class DirectionChoices(ChoiceSet):
    IN = "in"
    OUT = "out"
    ANY = "any"
    CHOICES = [(IN, "In"), (OUT, "Out"), (ANY, "Any")]


class IPProtocolChoices(ChoiceSet):
    INET = "inet"
    INET6 = "inet6"
    INET46 = "inet46"
    CHOICES = [(INET, "IPv4"), (INET6, "IPv6"), (INET46, "IPv4+IPv6")]


class EndpointTypeChoices(ChoiceSet):
    """How a rule's source/destination is interpreted (pf's polymorphic endpoint)."""
    ANY = "any"
    NETWORK = "network"          # a CIDR
    ADDRESS = "address"          # a single host
    ALIAS = "alias"             # references an Alias object
    SELF = "self"               # (self) — the firewall itself
    INTERFACE = "interface"      # an interface's subnet ("lan net")
    INTERFACE_IP = "interface_ip"  # an interface's address ("lan address" / "wanip")
    CHOICES = [
        (ANY, "Any"), (NETWORK, "Network (CIDR)"), (ADDRESS, "Address (host)"),
        (ALIAS, "Alias"), (SELF, "(self)"), (INTERFACE, "Interface net"),
        (INTERFACE_IP, "Interface IP"),
    ]


class AliasTypeChoices(ChoiceSet):
    HOST = "host"
    NETWORK = "network"
    PORT = "port"
    URL = "url"
    URLJSON = "urljson"
    GEOIP = "geoip"
    MAC = "mac"
    EXTERNAL = "external"
    CHOICES = [
        (HOST, "Host(s)"), (NETWORK, "Network(s)"), (PORT, "Port(s)"),
        (URL, "URL table"), (URLJSON, "URL table (JSON)"), (GEOIP, "GeoIP"),
        (MAC, "MAC"), (EXTERNAL, "External"),
    ]
