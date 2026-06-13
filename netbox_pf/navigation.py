# SPDX-License-Identifier: AGPL-3.0-or-later
from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

_rules = PluginMenuItem(
    link="plugins:netbox_pf:firewallrule_list",
    link_text="Firewall Rules",
    buttons=[PluginMenuButton("plugins:netbox_pf:firewallrule_add", "Add", "mdi mdi-plus-thick")],
)
_nat = PluginMenuItem(
    link="plugins:netbox_pf:natrule_list",
    link_text="NAT Rules",
    buttons=[PluginMenuButton("plugins:netbox_pf:natrule_add", "Add", "mdi mdi-plus-thick")],
)
_aliases = PluginMenuItem(
    link="plugins:netbox_pf:alias_list",
    link_text="Aliases",
    buttons=[PluginMenuButton("plugins:netbox_pf:alias_add", "Add", "mdi mdi-plus-thick")],
)

_gateways = PluginMenuItem(
    link="plugins:netbox_pf:gateway_list",
    link_text="Gateways",
    buttons=[PluginMenuButton("plugins:netbox_pf:gateway_add", "Add", "mdi mdi-plus-thick")],
)
_gw_groups = PluginMenuItem(
    link="plugins:netbox_pf:gatewaygroup_list",
    link_text="Gateway Groups",
    buttons=[PluginMenuButton("plugins:netbox_pf:gatewaygroup_add", "Add", "mdi mdi-plus-thick")],
)
_gw_members = PluginMenuItem(
    link="plugins:netbox_pf:gatewaygroupmember_list",
    link_text="Group Members",
    buttons=[PluginMenuButton("plugins:netbox_pf:gatewaygroupmember_add", "Add", "mdi mdi-plus-thick")],
)

menu = PluginMenu(
    label="Firewall (pf)",
    groups=(
        ("pf", (_rules, _nat, _aliases)),
        ("Routing", (_gateways, _gw_groups, _gw_members)),
    ),
    icon_class="mdi mdi-firewall",
)
