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


class NATTypeChoices(ChoiceSet):
    """pf NAT rule kind."""
    PORT_FORWARD = "port_forward"
    OUTBOUND = "outbound"
    ONE_TO_ONE = "one_to_one"
    CHOICES = [
        (PORT_FORWARD, "Port forward", "blue"),
        (OUTBOUND, "Outbound", "purple"),
        (ONE_TO_ONE, "1:1", "cyan"),
    ]


class AliasTypeChoices(ChoiceSet):
    """OPNsense/pfSense alias dialects (config.xml ``<aliases><alias><type>`` tokens)."""
    HOST = "host"
    NETWORK = "network"
    NETWORKGROUP = "networkgroup"
    PORT = "port"
    URL = "url"
    URLTABLE = "urltable"
    GEOIP = "geoip"
    MAC = "mac"
    ASN = "asn"
    DYNIPV6HOST = "dynipv6host"
    EXTERNAL = "external"
    INTERNAL = "internal"
    CHOICES = [
        (HOST, "Host(s)"), (NETWORK, "Network(s)"), (NETWORKGROUP, "Network group"),
        (PORT, "Port(s)"), (URL, "URL (download once)"), (URLTABLE, "URL table"),
        (GEOIP, "GeoIP"), (MAC, "MAC"), (ASN, "BGP ASN"),
        (DYNIPV6HOST, "Dynamic IPv6 host"), (EXTERNAL, "External"), (INTERNAL, "Internal"),
    ]


class GatewayTriggerChoices(ChoiceSet):
    """When a gateway-group member is considered down (pf gateway-group trigger level)."""

    DOWN = "down"
    DOWNLOSS = "downloss"
    DOWNLATENCY = "downlatency"
    DOWNLOSSLATENCY = "downlosslatency"
    CHOICES = [
        (DOWN, "Member down"),
        (DOWNLOSS, "Packet loss"),
        (DOWNLATENCY, "High latency"),
        (DOWNLOSSLATENCY, "Packet loss or high latency"),
    ]
