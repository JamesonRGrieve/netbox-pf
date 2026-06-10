# SPDX-License-Identifier: AGPL-3.0-or-later
"""FilterSet tests against a real DB (no mocks)."""
from django.test import TestCase
from utilities.testing import create_test_device
from netbox_pf.choices import AliasTypeChoices, EndpointTypeChoices, FirewallActionChoices
from netbox_pf.filtersets import AliasFilterSet, FirewallRuleFilterSet
from netbox_pf.models import Alias, FirewallRule


class AliasFilterSetTest(TestCase):
    queryset = Alias.objects.all()

    @classmethod
    def setUpTestData(cls):
        Alias.objects.bulk_create([
            Alias(name="Hosts", type=AliasTypeChoices.HOST, content="1.1.1.1"),
            Alias(name="Nets", type=AliasTypeChoices.NETWORK, content="10.0.0.0/8"),
            Alias(name="Ports", type=AliasTypeChoices.PORT, content="22,80"),
        ])

    def test_type(self):
        self.assertEqual(AliasFilterSet({"type": [AliasTypeChoices.HOST]}, self.queryset).qs.count(), 1)

    def test_search_name_and_content(self):
        self.assertEqual(AliasFilterSet({"q": "Hosts"}, self.queryset).qs.count(), 1)
        self.assertEqual(AliasFilterSet({"q": "10.0.0.0"}, self.queryset).qs.count(), 1)


class FirewallRuleFilterSetTest(TestCase):
    queryset = FirewallRule.objects.all()

    @classmethod
    def setUpTestData(cls):
        cls.device = create_test_device("fw1")
        FirewallRule.objects.bulk_create([
            FirewallRule(device=cls.device, sequence=0, action=FirewallActionChoices.PASS,
                         source_type=EndpointTypeChoices.ANY, destination_type=EndpointTypeChoices.SELF,
                         description="allow self"),
            FirewallRule(device=cls.device, sequence=1, action=FirewallActionChoices.BLOCK,
                         source_type=EndpointTypeChoices.ANY, destination_type=EndpointTypeChoices.ANY,
                         log=True, description="default block"),
            FirewallRule(device=cls.device, sequence=2, action=FirewallActionChoices.PASS,
                         source_type=EndpointTypeChoices.NETWORK, source="10.0.0.0/8",
                         destination_type=EndpointTypeChoices.ANY, interface="lan"),
        ])

    def test_action(self):
        self.assertEqual(FirewallRuleFilterSet({"action": [FirewallActionChoices.PASS]}, self.queryset).qs.count(), 2)

    def test_device(self):
        self.assertEqual(FirewallRuleFilterSet({"device": [self.device.pk]}, self.queryset).qs.count(), 3)

    def test_log_and_source_type(self):
        self.assertEqual(FirewallRuleFilterSet({"log": True}, self.queryset).qs.count(), 1)
        self.assertEqual(FirewallRuleFilterSet({"source_type": [EndpointTypeChoices.NETWORK]}, self.queryset).qs.count(), 1)

    def test_search(self):
        self.assertEqual(FirewallRuleFilterSet({"q": "default block"}, self.queryset).qs.count(), 1)
        self.assertEqual(FirewallRuleFilterSet({"q": "lan"}, self.queryset).qs.count(), 1)
