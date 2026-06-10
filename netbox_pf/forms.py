# SPDX-License-Identifier: AGPL-3.0-or-later
from dcim.models import Device
from django import forms
from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelForm
from utilities.forms.fields import (
    DynamicModelChoiceField, DynamicModelMultipleChoiceField, TagFilterField,
)
from utilities.forms.rendering import FieldSet
from .choices import AliasTypeChoices, DirectionChoices, FirewallActionChoices, IPProtocolChoices
from .models import Alias, FirewallRule


class AliasForm(NetBoxModelForm):
    class Meta:
        model = Alias
        fields = ["name", "type", "content", "detail", "description", "advanced", "tags"]


class FirewallRuleForm(NetBoxModelForm):
    device = DynamicModelChoiceField(queryset=Device.objects.all())
    source_alias = DynamicModelChoiceField(queryset=Alias.objects.all(), required=False)
    destination_alias = DynamicModelChoiceField(queryset=Alias.objects.all(), required=False)

    fieldsets = (
        FieldSet("device", "sequence", "action", "disabled", "quick", name="Rule"),
        FieldSet("interface", "floating", "direction", "ipprotocol", "protocol", name="Binding"),
        FieldSet("source_type", "source", "source_alias", "source_invert", "source_port", name="Source"),
        FieldSet("destination_type", "destination", "destination_alias", "destination_invert", "destination_port", name="Destination"),
        FieldSet("gateway", "log", "statetype", "sched", "tcpflags", "icmptype", "reply_to",
                 "tag", "tagged", "os", name="Advanced"),
        FieldSet("tracker", "uuid", "associated_rule_id", "advanced", name="Platform identity"),
        FieldSet("description", "tags", name="Misc"),
    )

    class Meta:
        model = FirewallRule
        fields = [
            "device", "sequence", "action", "disabled", "quick", "interface", "floating",
            "direction", "ipprotocol", "protocol", "source_type", "source", "source_alias",
            "source_invert", "source_port", "destination_type", "destination",
            "destination_alias", "destination_invert", "destination_port", "gateway", "log",
            "statetype", "sched", "tcpflags", "icmptype", "reply_to", "tag", "tagged", "os",
            "tracker", "uuid", "associated_rule_id", "advanced", "description", "tags",
        ]


class AliasFilterForm(NetBoxModelFilterSetForm):
    model = Alias
    type = forms.MultipleChoiceField(choices=AliasTypeChoices, required=False)
    tag = TagFilterField(Alias)


class FirewallRuleFilterForm(NetBoxModelFilterSetForm):
    model = FirewallRule
    device_id = DynamicModelMultipleChoiceField(queryset=Device.objects.all(), required=False, label="Device")
    action = forms.MultipleChoiceField(choices=FirewallActionChoices, required=False)
    direction = forms.MultipleChoiceField(choices=DirectionChoices, required=False)
    ipprotocol = forms.MultipleChoiceField(choices=IPProtocolChoices, required=False)
    disabled = forms.NullBooleanField(required=False)
    tag = TagFilterField(FirewallRule)
