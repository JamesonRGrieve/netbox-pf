# SPDX-License-Identifier: AGPL-3.0-or-later
import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from .models import Alias, FirewallRule, Gateway, GatewayGroup, GatewayGroupMember, NATRule


class AliasTable(NetBoxTable):
    name = tables.Column(linkify=True)
    tags = columns.TagColumn(url_name="plugins:netbox_pf:alias_list")

    class Meta(NetBoxTable.Meta):
        model = Alias
        fields = ("pk", "id", "name", "type", "content", "detail", "description", "advanced", "tags", "created", "last_updated")
        default_columns = ("name", "type", "description")


class FirewallRuleTable(NetBoxTable):
    device = tables.Column(linkify=True)
    sequence = tables.Column(linkify=True)
    action = columns.ChoiceFieldColumn()
    source_alias = tables.Column(linkify=True)
    destination_alias = tables.Column(linkify=True)
    tags = columns.TagColumn(url_name="plugins:netbox_pf:firewallrule_list")

    class Meta(NetBoxTable.Meta):
        model = FirewallRule
        fields = (
            "pk", "id", "device", "sequence", "action", "disabled", "quick", "interface",
            "floating", "direction", "ipprotocol", "protocol", "source_type", "source",
            "source_alias", "source_port", "destination_type", "destination",
            "destination_alias", "destination_port", "gateway", "log", "statetype",
            "sched", "tcpflags", "icmptype", "reply_to", "tag", "tagged", "os",
            "tracker", "uuid", "associated_rule_id", "description", "tags",
            "created", "last_updated",
        )
        default_columns = (
            "device", "sequence", "action", "interface", "protocol", "source",
            "destination", "destination_port", "description",
        )


class NATRuleTable(NetBoxTable):
    device = tables.Column(linkify=True)
    nat_type = columns.ChoiceFieldColumn()
    tags = columns.TagColumn(url_name="plugins:netbox_pf:natrule_list")

    class Meta(NetBoxTable.Meta):
        model = NATRule
        fields = (
            "pk", "id", "device", "nat_type", "sequence", "disabled", "interface",
            "ipprotocol", "protocol", "source", "source_port", "destination",
            "destination_port", "target", "local_port", "target_subnet", "external",
            "nat_port", "static_nat_port", "nonat", "nordr", "nosync", "natreflection",
            "poolopts", "associated_rule_id", "description", "advanced", "tags",
            "created", "last_updated",
        )
        default_columns = (
            "device", "nat_type", "sequence", "interface", "protocol", "source",
            "destination", "destination_port", "target", "local_port", "description",
        )


class GatewayTable(NetBoxTable):
    device = tables.Column(linkify=True)
    name = tables.Column(linkify=True)
    tags = columns.TagColumn(url_name="plugins:netbox_pf:gateway_list")

    class Meta(NetBoxTable.Meta):
        model = Gateway
        fields = (
            "pk", "id", "device", "name", "interface", "address", "ipprotocol", "monitor_ip",
            "weight", "priority", "far_gateway", "default_gateway", "disabled", "description",
            "tags", "created", "last_updated",
        )
        default_columns = ("device", "name", "interface", "address", "priority", "default_gateway")


class GatewayGroupTable(NetBoxTable):
    device = tables.Column(linkify=True)
    name = tables.Column(linkify=True)
    tags = columns.TagColumn(url_name="plugins:netbox_pf:gatewaygroup_list")

    class Meta(NetBoxTable.Meta):
        model = GatewayGroup
        fields = ("pk", "id", "device", "name", "trigger", "description", "tags", "created", "last_updated")
        default_columns = ("device", "name", "trigger")


class GatewayGroupMemberTable(NetBoxTable):
    group = tables.Column(linkify=True)
    gateway = tables.Column(linkify=True)
    tags = columns.TagColumn(url_name="plugins:netbox_pf:gatewaygroupmember_list")

    class Meta(NetBoxTable.Meta):
        model = GatewayGroupMember
        fields = ("pk", "id", "group", "gateway", "tier", "tags", "created", "last_updated")
        default_columns = ("group", "gateway", "tier")
