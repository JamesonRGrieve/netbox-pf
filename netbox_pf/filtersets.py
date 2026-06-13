# SPDX-License-Identifier: AGPL-3.0-or-later
import django_filters
from dcim.models import Device
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from .models import Alias, FirewallRule, Gateway, GatewayGroup, GatewayGroupMember, NATRule


class AliasFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Alias
        fields = ["id", "name", "type"]

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(content__icontains=value) | Q(description__icontains=value)
        )


class FirewallRuleFilterSet(NetBoxModelFilterSet):
    # Explicit FK filters: django-filter does NOT derive `<fk>_id` from a bare FK in
    # Meta.fields, so `?device_id=` was silently ignored (returned all rules). NetBox
    # convention is `<fk>_id` (by PK) + `<fk>` (by natural key).
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name="device", queryset=Device.objects.all(), label="Device (ID)",
    )
    device = django_filters.ModelMultipleChoiceFilter(
        field_name="device__name", to_field_name="name", queryset=Device.objects.all(),
        label="Device (name)",
    )
    source_alias_id = django_filters.ModelMultipleChoiceFilter(
        field_name="source_alias", queryset=Alias.objects.all(), label="Source alias (ID)",
    )
    destination_alias_id = django_filters.ModelMultipleChoiceFilter(
        field_name="destination_alias", queryset=Alias.objects.all(), label="Destination alias (ID)",
    )

    class Meta:
        model = FirewallRule
        fields = [
            "id", "sequence", "action", "disabled", "quick", "interface",
            "floating", "direction", "ipprotocol", "protocol", "source_type", "source",
            "destination_type", "destination", "gateway", "log", "tag", "tagged", "os",
            "tracker", "uuid",
        ]

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(description__icontains=value) | Q(interface__icontains=value)
            | Q(source__icontains=value) | Q(destination__icontains=value)
            | Q(gateway__icontains=value)
        )


class NATRuleFilterSet(NetBoxModelFilterSet):
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name="device", queryset=Device.objects.all(), label="Device (ID)",
    )
    device = django_filters.ModelMultipleChoiceFilter(
        field_name="device__name", to_field_name="name", queryset=Device.objects.all(),
        label="Device (name)",
    )

    class Meta:
        model = NATRule
        fields = [
            "id", "nat_type", "sequence", "disabled", "interface", "ipprotocol",
            "protocol", "source", "destination", "target", "description",
        ]

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(description__icontains=value) | Q(interface__icontains=value)
            | Q(source__icontains=value) | Q(destination__icontains=value)
            | Q(target__icontains=value)
        )


class GatewayFilterSet(NetBoxModelFilterSet):
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name="device", queryset=Device.objects.all(), label="Device (ID)"
    )
    device = django_filters.ModelMultipleChoiceFilter(
        field_name="device__name", to_field_name="name", queryset=Device.objects.all(), label="Device (name)"
    )

    class Meta:
        model = Gateway
        fields = ["id", "name", "interface", "address", "ipprotocol", "priority", "default_gateway", "disabled"]

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(interface__icontains=value) | Q(description__icontains=value)
        )


class GatewayGroupFilterSet(NetBoxModelFilterSet):
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name="device", queryset=Device.objects.all(), label="Device (ID)"
    )
    device = django_filters.ModelMultipleChoiceFilter(
        field_name="device__name", to_field_name="name", queryset=Device.objects.all(), label="Device (name)"
    )

    class Meta:
        model = GatewayGroup
        fields = ["id", "name", "trigger"]

    def search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))


class GatewayGroupMemberFilterSet(NetBoxModelFilterSet):
    group_id = django_filters.ModelMultipleChoiceFilter(
        field_name="group", queryset=GatewayGroup.objects.all(), label="Group (ID)"
    )
    gateway_id = django_filters.ModelMultipleChoiceFilter(
        field_name="gateway", queryset=Gateway.objects.all(), label="Gateway (ID)"
    )

    class Meta:
        model = GatewayGroupMember
        fields = ["id", "tier"]

    def search(self, queryset, name, value):
        return queryset.filter(Q(group__name__icontains=value) | Q(gateway__name__icontains=value))
