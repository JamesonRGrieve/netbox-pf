# SPDX-License-Identifier: AGPL-3.0-or-later
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from .models import Alias, FirewallRule


class AliasFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Alias
        fields = ["id", "name", "type"]

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(content__icontains=value) | Q(description__icontains=value)
        )


class FirewallRuleFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = FirewallRule
        fields = [
            "id", "device", "sequence", "action", "disabled", "quick", "interface",
            "floating", "direction", "ipprotocol", "protocol", "source_type", "source",
            "source_alias", "destination_type", "destination", "destination_alias",
            "gateway", "log", "tag", "tagged", "os", "tracker", "uuid",
        ]

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(description__icontains=value) | Q(interface__icontains=value)
            | Q(source__icontains=value) | Q(destination__icontains=value)
            | Q(gateway__icontains=value)
        )
