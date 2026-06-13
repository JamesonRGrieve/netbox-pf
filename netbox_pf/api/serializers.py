# SPDX-License-Identifier: AGPL-3.0-or-later
from dcim.api.serializers import DeviceSerializer
from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers
from ..models import Alias, FirewallRule, Gateway, GatewayGroup, GatewayGroupMember, NATRule


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


class NATRuleSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_pf-api:natrule-detail")
    device = DeviceSerializer(nested=True)

    class Meta:
        model = NATRule
        fields = [
            "id", "url", "display", "device", "nat_type", "sequence", "disabled",
            "interface", "ipprotocol", "protocol", "source", "source_port",
            "destination", "destination_port", "target", "local_port", "target_subnet",
            "external", "nat_port", "static_nat_port", "nonat", "nordr", "nosync",
            "natreflection", "poolopts", "associated_rule_id", "description", "advanced",
            "tags", "custom_fields", "created", "last_updated",
        ]
        brief_fields = ["id", "url", "display", "device", "nat_type", "sequence"]


class GatewaySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_pf-api:gateway-detail")
    device = DeviceSerializer(nested=True)

    class Meta:
        model = Gateway
        fields = [
            "id", "url", "display", "device", "name", "interface", "address", "ipprotocol",
            "monitor_ip", "weight", "priority", "far_gateway", "default_gateway", "disabled",
            "description", "tags", "custom_fields", "created", "last_updated",
        ]
        brief_fields = ["id", "url", "display", "device", "name"]


class GatewayGroupSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_pf-api:gatewaygroup-detail")
    device = DeviceSerializer(nested=True)

    class Meta:
        model = GatewayGroup
        fields = [
            "id", "url", "display", "device", "name", "trigger", "description",
            "tags", "custom_fields", "created", "last_updated",
        ]
        brief_fields = ["id", "url", "display", "device", "name"]


class GatewayGroupMemberSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_pf-api:gatewaygroupmember-detail")
    group = GatewayGroupSerializer(nested=True)
    gateway = GatewaySerializer(nested=True)

    class Meta:
        model = GatewayGroupMember
        fields = [
            "id", "url", "display", "group", "gateway", "tier",
            "tags", "custom_fields", "created", "last_updated",
        ]
        brief_fields = ["id", "url", "display", "group", "gateway", "tier"]
