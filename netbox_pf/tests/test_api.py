# SPDX-License-Identifier: AGPL-3.0-or-later
"""REST API CRUD tests against a real DB + real API client (no mocks).

Composes the explicit CRUD mixins (not the GraphQL-inclusive APIViewTestCase) since the
plugin ships no GraphQL type yet.
"""
from utilities.testing import APIViewTestCases, create_test_device
from netbox_pf.models import Alias, FirewallRule, NATRule


class _CRUD(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    pass


class AliasAPITest(_CRUD):
    model = Alias
    brief_fields = ["display", "id", "name", "type", "url"]
    create_data = [
        {"name": "WebServers", "type": "host", "content": "192.0.2.10\n192.0.2.11"},
        {"name": "MgmtNets", "type": "network", "content": "10.0.0.0/8"},
        {"name": "HTTPPorts", "type": "port", "content": "80,443"},
    ]
    bulk_update_data = {"description": "bulk-updated"}

    @classmethod
    def setUpTestData(cls):
        Alias.objects.bulk_create([
            Alias(name="A1", type="host", content="1.1.1.1"),
            Alias(name="A2", type="network", content="10.0.0.0/8"),
            Alias(name="A3", type="port", content="22"),
        ])


class FirewallRuleAPITest(_CRUD):
    model = FirewallRule
    brief_fields = ["action", "device", "display", "id", "sequence", "url"]
    bulk_update_data = {"log": True}

    @classmethod
    def setUpTestData(cls):
        device = create_test_device("fw1")
        FirewallRule.objects.bulk_create([
            FirewallRule(device=device, sequence=0, action="pass", destination_type="self"),
            FirewallRule(device=device, sequence=1, action="block"),
            FirewallRule(device=device, sequence=2, action="pass", source_type="network", source="10.0.0.0/8"),
        ])
        cls.create_data = [
            {"device": device.pk, "sequence": 10, "action": "pass", "source_type": "any", "destination_type": "any"},
            {"device": device.pk, "sequence": 11, "action": "block", "source_type": "network",
             "source": "192.0.2.0/24", "destination_type": "self"},
            {"device": device.pk, "sequence": 12, "action": "reject", "source_type": "any",
             "destination_type": "any", "gateway": "WAN_GW", "quick": True, "log": True},
        ]


class NATRuleAPITest(_CRUD):
    model = NATRule
    brief_fields = ["device", "display", "id", "nat_type", "sequence", "url"]
    bulk_update_data = {"disabled": True}

    @classmethod
    def setUpTestData(cls):
        device = create_test_device("nat1")
        NATRule.objects.bulk_create([
            NATRule(device=device, nat_type="port_forward", sequence=0, interface="wan",
                    destination="wan:ip", destination_port="443", target="192.0.2.10", local_port="443"),
            NATRule(device=device, nat_type="outbound", sequence=0, interface="wan",
                    source="10.0.0.0/8", target="wan:ip"),
            NATRule(device=device, nat_type="one_to_one", sequence=0, interface="wan",
                    external="203.0.113.10", destination="192.0.2.10"),
        ])
        cls.create_data = [
            {"device": device.pk, "nat_type": "port_forward", "sequence": 10, "interface": "wan",
             "destination": "wan:ip", "destination_port": "8443", "target": "192.0.2.20", "local_port": "8443"},
            {"device": device.pk, "nat_type": "outbound", "sequence": 10, "interface": "wan",
             "source": "192.168.0.0/16", "target": "wan:ip", "static_nat_port": True},
            {"device": device.pk, "nat_type": "one_to_one", "sequence": 10, "interface": "wan",
             "external": "203.0.113.20", "destination": "192.0.2.21"},
        ]
