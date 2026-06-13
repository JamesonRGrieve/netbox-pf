# SPDX-License-Identifier: AGPL-3.0-or-later
from netbox.views import generic
from . import filtersets, forms, models, tables


class AliasView(generic.ObjectView):
    queryset = models.Alias.objects.all()


class AliasListView(generic.ObjectListView):
    queryset = models.Alias.objects.all()
    table = tables.AliasTable
    filterset = filtersets.AliasFilterSet
    filterset_form = forms.AliasFilterForm


class AliasEditView(generic.ObjectEditView):
    queryset = models.Alias.objects.all()
    form = forms.AliasForm


class AliasDeleteView(generic.ObjectDeleteView):
    queryset = models.Alias.objects.all()


class AliasBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Alias.objects.all()
    table = tables.AliasTable


class FirewallRuleView(generic.ObjectView):
    queryset = models.FirewallRule.objects.all()


class FirewallRuleListView(generic.ObjectListView):
    queryset = models.FirewallRule.objects.all()
    table = tables.FirewallRuleTable
    filterset = filtersets.FirewallRuleFilterSet
    filterset_form = forms.FirewallRuleFilterForm


class FirewallRuleEditView(generic.ObjectEditView):
    queryset = models.FirewallRule.objects.all()
    form = forms.FirewallRuleForm


class FirewallRuleDeleteView(generic.ObjectDeleteView):
    queryset = models.FirewallRule.objects.all()


class FirewallRuleBulkDeleteView(generic.BulkDeleteView):
    queryset = models.FirewallRule.objects.all()
    table = tables.FirewallRuleTable


class NATRuleView(generic.ObjectView):
    queryset = models.NATRule.objects.all()


class NATRuleListView(generic.ObjectListView):
    queryset = models.NATRule.objects.all()
    table = tables.NATRuleTable
    filterset = filtersets.NATRuleFilterSet
    filterset_form = forms.NATRuleFilterForm


class NATRuleEditView(generic.ObjectEditView):
    queryset = models.NATRule.objects.all()
    form = forms.NATRuleForm


class NATRuleDeleteView(generic.ObjectDeleteView):
    queryset = models.NATRule.objects.all()


class NATRuleBulkDeleteView(generic.BulkDeleteView):
    queryset = models.NATRule.objects.all()
    table = tables.NATRuleTable


class GatewayView(generic.ObjectView):
    queryset = models.Gateway.objects.all()


class GatewayListView(generic.ObjectListView):
    queryset = models.Gateway.objects.all()
    table = tables.GatewayTable
    filterset = filtersets.GatewayFilterSet
    filterset_form = forms.GatewayFilterForm


class GatewayEditView(generic.ObjectEditView):
    queryset = models.Gateway.objects.all()
    form = forms.GatewayForm


class GatewayDeleteView(generic.ObjectDeleteView):
    queryset = models.Gateway.objects.all()


class GatewayBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Gateway.objects.all()
    table = tables.GatewayTable


class GatewayGroupView(generic.ObjectView):
    queryset = models.GatewayGroup.objects.all()


class GatewayGroupListView(generic.ObjectListView):
    queryset = models.GatewayGroup.objects.all()
    table = tables.GatewayGroupTable
    filterset = filtersets.GatewayGroupFilterSet
    filterset_form = forms.GatewayGroupFilterForm


class GatewayGroupEditView(generic.ObjectEditView):
    queryset = models.GatewayGroup.objects.all()
    form = forms.GatewayGroupForm


class GatewayGroupDeleteView(generic.ObjectDeleteView):
    queryset = models.GatewayGroup.objects.all()


class GatewayGroupBulkDeleteView(generic.BulkDeleteView):
    queryset = models.GatewayGroup.objects.all()
    table = tables.GatewayGroupTable


class GatewayGroupMemberView(generic.ObjectView):
    queryset = models.GatewayGroupMember.objects.all()


class GatewayGroupMemberListView(generic.ObjectListView):
    queryset = models.GatewayGroupMember.objects.all()
    table = tables.GatewayGroupMemberTable
    filterset = filtersets.GatewayGroupMemberFilterSet
    filterset_form = forms.GatewayGroupMemberFilterForm


class GatewayGroupMemberEditView(generic.ObjectEditView):
    queryset = models.GatewayGroupMember.objects.all()
    form = forms.GatewayGroupMemberForm


class GatewayGroupMemberDeleteView(generic.ObjectDeleteView):
    queryset = models.GatewayGroupMember.objects.all()


class GatewayGroupMemberBulkDeleteView(generic.BulkDeleteView):
    queryset = models.GatewayGroupMember.objects.all()
    table = tables.GatewayGroupMemberTable
