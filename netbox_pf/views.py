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
