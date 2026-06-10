# SPDX-License-Identifier: AGPL-3.0-or-later
from netbox.api.viewsets import NetBoxModelViewSet
from .. import filtersets
from ..models import Alias, FirewallRule
from .serializers import AliasSerializer, FirewallRuleSerializer


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
