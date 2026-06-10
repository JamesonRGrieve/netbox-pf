# SPDX-License-Identifier: AGPL-3.0-or-later
from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

_rules = PluginMenuItem(
    link="plugins:netbox_pf:firewallrule_list",
    link_text="Firewall Rules",
    buttons=[PluginMenuButton("plugins:netbox_pf:firewallrule_add", "Add", "mdi mdi-plus-thick")],
)
_aliases = PluginMenuItem(
    link="plugins:netbox_pf:alias_list",
    link_text="Aliases",
    buttons=[PluginMenuButton("plugins:netbox_pf:alias_add", "Add", "mdi mdi-plus-thick")],
)

menu = PluginMenu(
    label="Firewall (pf)",
    groups=(("pf", (_rules, _aliases)),),
    icon_class="mdi mdi-firewall",
)
