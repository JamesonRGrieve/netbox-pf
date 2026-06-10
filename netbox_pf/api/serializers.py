# SPDX-License-Identifier: AGPL-3.0-or-later
from dcim.api.serializers import DeviceSerializer
from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers
from ..models import Alias, FirewallRule


class AliasSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_pf-api:alias-detail")

    class Meta:
        model = Alias
        fields = [
            "id", "url", "display", "name", "type", "content", "detail", "description",
            "advanced", "tags", "custom_fields", "created", "last_updated",
        ]
        brief_fields = ["id", "url", "display", "name", "type"]


class FirewallRuleSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_pf-api:firewallrule-detail")
    device = DeviceSerializer(nested=True)
    source_alias = AliasSerializer(nested=True, required=False, allow_null=True)
    destination_alias = AliasSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = FirewallRule
        fields = [
            "id", "url", "display", "device", "sequence", "action", "disabled", "quick",
            "interface", "floating", "direction", "ipprotocol", "protocol",
            "source_type", "source", "source_alias", "source_invert", "source_port",
            "destination_type", "destination", "destination_alias", "destination_invert",
            "destination_port", "gateway", "log", "statetype", "sched", "tcpflags",
            "icmptype", "reply_to", "tag", "tagged", "os", "description",
            "tracker", "uuid", "associated_rule_id", "advanced",
            "tags", "custom_fields", "created", "last_updated",
        ]
        brief_fields = ["id", "url", "display", "device", "sequence", "action"]
