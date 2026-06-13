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
    # NAT rules
    path("nat-rules/", views.NATRuleListView.as_view(), name="natrule_list"),
    path("nat-rules/add/", views.NATRuleEditView.as_view(), name="natrule_add"),
    path("nat-rules/delete/", views.NATRuleBulkDeleteView.as_view(), name="natrule_bulk_delete"),
    path("nat-rules/<int:pk>/", views.NATRuleView.as_view(), name="natrule"),
    path("nat-rules/<int:pk>/edit/", views.NATRuleEditView.as_view(), name="natrule_edit"),
    path("nat-rules/<int:pk>/delete/", views.NATRuleDeleteView.as_view(), name="natrule_delete"),
    path("nat-rules/<int:pk>/changelog/", ObjectChangeLogView.as_view(), name="natrule_changelog", kwargs={"model": models.NATRule}),
    path("nat-rules/<int:pk>/journal/", ObjectJournalView.as_view(), name="natrule_journal", kwargs={"model": models.NATRule}),
    # Gateways
    path("gateways/", views.GatewayListView.as_view(), name="gateway_list"),
    path("gateways/add/", views.GatewayEditView.as_view(), name="gateway_add"),
    path("gateways/delete/", views.GatewayBulkDeleteView.as_view(), name="gateway_bulk_delete"),
    path("gateways/<int:pk>/", views.GatewayView.as_view(), name="gateway"),
    path("gateways/<int:pk>/edit/", views.GatewayEditView.as_view(), name="gateway_edit"),
    path("gateways/<int:pk>/delete/", views.GatewayDeleteView.as_view(), name="gateway_delete"),
    path("gateways/<int:pk>/changelog/", ObjectChangeLogView.as_view(), name="gateway_changelog", kwargs={"model": models.Gateway}),
    path("gateways/<int:pk>/journal/", ObjectJournalView.as_view(), name="gateway_journal", kwargs={"model": models.Gateway}),
    # Gateway groups
    path("gateway-groups/", views.GatewayGroupListView.as_view(), name="gatewaygroup_list"),
    path("gateway-groups/add/", views.GatewayGroupEditView.as_view(), name="gatewaygroup_add"),
    path("gateway-groups/delete/", views.GatewayGroupBulkDeleteView.as_view(), name="gatewaygroup_bulk_delete"),
    path("gateway-groups/<int:pk>/", views.GatewayGroupView.as_view(), name="gatewaygroup"),
    path("gateway-groups/<int:pk>/edit/", views.GatewayGroupEditView.as_view(), name="gatewaygroup_edit"),
    path("gateway-groups/<int:pk>/delete/", views.GatewayGroupDeleteView.as_view(), name="gatewaygroup_delete"),
    path("gateway-groups/<int:pk>/changelog/", ObjectChangeLogView.as_view(), name="gatewaygroup_changelog", kwargs={"model": models.GatewayGroup}),
    path("gateway-groups/<int:pk>/journal/", ObjectJournalView.as_view(), name="gatewaygroup_journal", kwargs={"model": models.GatewayGroup}),
    # Gateway group members
    path("gateway-group-members/", views.GatewayGroupMemberListView.as_view(), name="gatewaygroupmember_list"),
    path("gateway-group-members/add/", views.GatewayGroupMemberEditView.as_view(), name="gatewaygroupmember_add"),
    path("gateway-group-members/delete/", views.GatewayGroupMemberBulkDeleteView.as_view(), name="gatewaygroupmember_bulk_delete"),
    path("gateway-group-members/<int:pk>/", views.GatewayGroupMemberView.as_view(), name="gatewaygroupmember"),
    path("gateway-group-members/<int:pk>/edit/", views.GatewayGroupMemberEditView.as_view(), name="gatewaygroupmember_edit"),
    path("gateway-group-members/<int:pk>/delete/", views.GatewayGroupMemberDeleteView.as_view(), name="gatewaygroupmember_delete"),
    path("gateway-group-members/<int:pk>/changelog/", ObjectChangeLogView.as_view(), name="gatewaygroupmember_changelog", kwargs={"model": models.GatewayGroupMember}),
    path("gateway-group-members/<int:pk>/journal/", ObjectJournalView.as_view(), name="gatewaygroupmember_journal", kwargs={"model": models.GatewayGroupMember}),
]
