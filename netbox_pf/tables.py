# SPDX-License-Identifier: AGPL-3.0-or-later
import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from .models import Alias, FirewallRule


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
