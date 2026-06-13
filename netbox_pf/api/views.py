# SPDX-License-Identifier: AGPL-3.0-or-later
from netbox.api.viewsets import NetBoxModelViewSet
from .. import filtersets
from ..models import Alias, FirewallRule, Gateway, GatewayGroup, GatewayGroupMember, NATRule
from .serializers import (
    AliasSerializer, FirewallRuleSerializer, GatewayGroupMemberSerializer, GatewayGroupSerializer,
    GatewaySerializer, NATRuleSerializer,
)


class AliasViewSet(NetBoxModelViewSet):
    queryset = Alias.objects.prefetch_related("tags")
    serializer_class = AliasSerializer
    filterset_class = filtersets.AliasFilterSet


class FirewallRuleViewSet(NetBoxModelViewSet):
    queryset = FirewallRule.objects.prefetch_related(
        "device", "source_alias", "destination_alias", "tags"
    )
    serializer_class = FirewallRuleSerializer
    filterset_class = filtersets.FirewallRuleFilterSet


class NATRuleViewSet(NetBoxModelViewSet):
    queryset = NATRule.objects.prefetch_related("device", "tags")
    serializer_class = NATRuleSerializer
    filterset_class = filtersets.NATRuleFilterSet


class GatewayViewSet(NetBoxModelViewSet):
    queryset = Gateway.objects.prefetch_related("device", "tags")
    serializer_class = GatewaySerializer
    filterset_class = filtersets.GatewayFilterSet


class GatewayGroupViewSet(NetBoxModelViewSet):
    queryset = GatewayGroup.objects.prefetch_related("device", "tags")
    serializer_class = GatewayGroupSerializer
    filterset_class = filtersets.GatewayGroupFilterSet


class GatewayGroupMemberViewSet(NetBoxModelViewSet):
    queryset = GatewayGroupMember.objects.prefetch_related("group", "gateway", "tags")
    serializer_class = GatewayGroupMemberSerializer
    filterset_class = filtersets.GatewayGroupMemberFilterSet
