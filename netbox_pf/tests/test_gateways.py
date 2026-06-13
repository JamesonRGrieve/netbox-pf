# SPDX-License-Identifier: AGPL-3.0-or-later
"""Gateway model tests against a real DB (no mocks): uniqueness, failover tiers, PROTECT."""
from django.db import transaction
from django.db.models import ProtectedError
from django.db.utils import IntegrityError
from django.test import TestCase
from utilities.testing import create_test_device
from netbox_pf.models import Gateway, GatewayGroup, GatewayGroupMember


class GatewayModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.device = create_test_device("fw1")

    def test_create_str_url(self):
        g = Gateway.objects.create(device=self.device, name="WAN_TELUS", interface="wan", address="192.168.2.1")
        self.assertEqual(str(g), f"{self.device}: WAN_TELUS")
        self.assertIn("/plugins/pf/gateways/", g.get_absolute_url())

    def test_unique_device_name(self):
        Gateway.objects.create(device=self.device, name="WAN", interface="wan", address="1.1.1.1")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Gateway.objects.create(device=self.device, name="WAN", interface="wan2", address="2.2.2.2")

    def test_dynamic_gateway_blank_address(self):
        g = Gateway.objects.create(device=self.device, name="WAN_DHCP", interface="wan")
        self.assertIsNone(g.address)
        self.assertEqual(g.weight, 1)
        self.assertEqual(g.priority, 255)


class GatewayGroupModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.device = create_test_device("fw1")
        cls.wan1 = Gateway.objects.create(device=cls.device, name="WAN_TELUS", interface="wan", address="192.168.2.1")
        cls.wan2 = Gateway.objects.create(device=cls.device, name="WAN_STARLINK", interface="wan2", address="192.168.3.1")

    def test_failover_tiers(self):
        grp = GatewayGroup.objects.create(device=self.device, name="WAN_FAILOVER")
        GatewayGroupMember.objects.create(group=grp, gateway=self.wan1, tier=1)
        GatewayGroupMember.objects.create(group=grp, gateway=self.wan2, tier=2)
        self.assertEqual(grp.members.count(), 2)
        self.assertEqual(grp.members.first().gateway, self.wan1)  # ordered by tier

    def test_gateway_protected_while_in_group(self):
        grp = GatewayGroup.objects.create(device=self.device, name="GRP")
        GatewayGroupMember.objects.create(group=grp, gateway=self.wan1, tier=1)
        with self.assertRaises(ProtectedError), transaction.atomic():
            self.wan1.delete()

    def test_member_unique_per_group(self):
        grp = GatewayGroup.objects.create(device=self.device, name="GRP2")
        GatewayGroupMember.objects.create(group=grp, gateway=self.wan1, tier=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            GatewayGroupMember.objects.create(group=grp, gateway=self.wan1, tier=2)
