# SPDX-License-Identifier: AGPL-3.0-or-later
"""Model tests against a real DB (no mocks): creation, str, constraints, FK behaviour."""
from django.db import transaction
from django.db.models import ProtectedError
from django.db.utils import IntegrityError
from django.test import TestCase
from utilities.testing import create_test_device
from netbox_pf.choices import (
    AliasTypeChoices, EndpointTypeChoices, FirewallActionChoices, NATTypeChoices,
)
from netbox_pf.models import Alias, FirewallRule, NATRule


class AliasModelTest(TestCase):
    def test_create_str_and_url(self):
        a = Alias.objects.create(name="WebServers", type=AliasTypeChoices.HOST, content="192.0.2.10")
        self.assertEqual(str(a), "WebServers")
        self.assertIn("/plugins/pf/aliases/", a.get_absolute_url())

    def test_name_unique(self):
        Alias.objects.create(name="dup", type=AliasTypeChoices.HOST, content="1.1.1.1")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Alias.objects.create(name="dup", type=AliasTypeChoices.NETWORK, content="10.0.0.0/8")


class FirewallRuleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.device = create_test_device("fw1")

    def test_create_str_and_url(self):
        r = FirewallRule.objects.create(device=self.device, sequence=5, action=FirewallActionChoices.PASS)
        self.assertEqual(str(r), f"{self.device}: 0005 pass")
        self.assertIn("/plugins/pf/firewall-rules/", r.get_absolute_url())
        self.assertEqual(r.get_action_color(), "green")

    def test_defaults(self):
        r = FirewallRule.objects.create(device=self.device, sequence=0, action=FirewallActionChoices.BLOCK)
        self.assertTrue(r.quick)
        self.assertFalse(r.disabled)
        self.assertEqual(r.source_type, EndpointTypeChoices.ANY)
        self.assertEqual(r.direction, "in")

    def test_unique_sequence_per_device(self):
        FirewallRule.objects.create(device=self.device, sequence=1, action=FirewallActionChoices.PASS)
        with self.assertRaises(IntegrityError), transaction.atomic():
            FirewallRule.objects.create(device=self.device, sequence=1, action=FirewallActionChoices.BLOCK)

    def test_alias_fk_and_protect(self):
        alias = Alias.objects.create(name="WG", type=AliasTypeChoices.PORT, content="51820")
        r = FirewallRule.objects.create(
            device=self.device, sequence=2, action=FirewallActionChoices.PASS,
            source_type=EndpointTypeChoices.ALIAS, source_alias=alias,
        )
        self.assertEqual(r.source_alias, alias)
        with self.assertRaises(ProtectedError), transaction.atomic():
            alias.delete()

    def test_cross_platform_fields_roundtrip(self):
        """pfSense (tracker) and OPNsense (uuid) identities + the advanced JSON survive."""
        r1 = FirewallRule.objects.create(
            device=self.device, sequence=10, action=FirewallActionChoices.PASS,
            tracker="1700000000", advanced={"max-states": 500, "statetimeout": 30, "sloppy": True},
        )
        r2 = FirewallRule.objects.create(
            device=self.device, sequence=11, action=FirewallActionChoices.BLOCK,
            uuid="b1e2c3d4-0000-1111-2222-333344445555", tagged="trusted", os="Linux",
        )
        r1.refresh_from_db()
        r2.refresh_from_db()
        self.assertEqual(r1.tracker, "1700000000")
        self.assertEqual(r1.advanced, {"max-states": 500, "statetimeout": 30, "sloppy": True})
        self.assertEqual(r2.uuid, "b1e2c3d4-0000-1111-2222-333344445555")
        self.assertEqual(r2.tagged, "trusted")
        self.assertEqual(r2.os, "Linux")


class NATRuleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.device = create_test_device("nat1")

    def test_create_str_url_color(self):
        n = NATRule.objects.create(
            device=self.device, nat_type=NATTypeChoices.PORT_FORWARD, sequence=0,
            interface="wan", target="192.0.2.10", local_port="443",
        )
        self.assertEqual(str(n), f"{self.device}: port_forward 0000")
        self.assertIn("/plugins/pf/nat-rules/", n.get_absolute_url())
        self.assertEqual(n.get_nat_type_color(), "blue")

    def test_unique_type_sequence_per_device(self):
        NATRule.objects.create(device=self.device, nat_type=NATTypeChoices.OUTBOUND, sequence=0)
        with self.assertRaises(IntegrityError), transaction.atomic():
            NATRule.objects.create(device=self.device, nat_type=NATTypeChoices.OUTBOUND, sequence=0)
        # same sequence under a different nat_type is allowed
        other = NATRule.objects.create(device=self.device, nat_type=NATTypeChoices.PORT_FORWARD, sequence=0)
        self.assertEqual(other.sequence, 0)
