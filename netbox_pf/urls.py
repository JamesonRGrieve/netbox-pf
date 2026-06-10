# SPDX-License-Identifier: AGPL-3.0-or-later
from django.urls import path
from netbox.views.generic import ObjectChangeLogView, ObjectJournalView
from . import models, views

urlpatterns = [
    # Aliases
    path("aliases/", views.AliasListView.as_view(), name="alias_list"),
    path("aliases/add/", views.AliasEditView.as_view(), name="alias_add"),
    path("aliases/delete/", views.AliasBulkDeleteView.as_view(), name="alias_bulk_delete"),
    path("aliases/<int:pk>/", views.AliasView.as_view(), name="alias"),
    path("aliases/<int:pk>/edit/", views.AliasEditView.as_view(), name="alias_edit"),
    path("aliases/<int:pk>/delete/", views.AliasDeleteView.as_view(), name="alias_delete"),
    path("aliases/<int:pk>/changelog/", ObjectChangeLogView.as_view(), name="alias_changelog", kwargs={"model": models.Alias}),
    path("aliases/<int:pk>/journal/", ObjectJournalView.as_view(), name="alias_journal", kwargs={"model": models.Alias}),
    # Firewall rules
    path("firewall-rules/", views.FirewallRuleListView.as_view(), name="firewallrule_list"),
    path("firewall-rules/add/", views.FirewallRuleEditView.as_view(), name="firewallrule_add"),
    path("firewall-rules/delete/", views.FirewallRuleBulkDeleteView.as_view(), name="firewallrule_bulk_delete"),
    path("firewall-rules/<int:pk>/", views.FirewallRuleView.as_view(), name="firewallrule"),
    path("firewall-rules/<int:pk>/edit/", views.FirewallRuleEditView.as_view(), name="firewallrule_edit"),
    path("firewall-rules/<int:pk>/delete/", views.FirewallRuleDeleteView.as_view(), name="firewallrule_delete"),
    path("firewall-rules/<int:pk>/changelog/", ObjectChangeLogView.as_view(), name="firewallrule_changelog", kwargs={"model": models.FirewallRule}),
    path("firewall-rules/<int:pk>/journal/", ObjectJournalView.as_view(), name="firewallrule_journal", kwargs={"model": models.FirewallRule}),
]
