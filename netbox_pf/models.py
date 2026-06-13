# SPDX-License-Identifier: AGPL-3.0-or-later
"""Native pf/OPNsense firewall model. Each pf field is a real column → zero-loss SoT."""
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from .choices import (
    AliasTypeChoices, DirectionChoices, EndpointTypeChoices,
    FirewallActionChoices, GatewayTriggerChoices, IPProtocolChoices, NATTypeChoices,
)


class Alias(NetBoxModel):
    """A pf alias: a named, typed group of hosts/networks/ports/urls referenced by rules.

    Covers both OPNsense and pfSense alias dialects; the long-tail (proto, dynamic
    interface, categories, …) lives in ``advanced`` for zero-loss round-trip.
    """
    name = models.CharField(max_length=128, unique=True)
    type = models.CharField(max_length=16, choices=AliasTypeChoices)
    content = models.TextField(
        blank=True,
        help_text="Members, one per line or comma-separated; may name other aliases (nesting).",
    )
    detail = models.TextField(blank=True, help_text="Per-member descriptions (pfSense), aligned to content.")
    description = models.CharField(max_length=200, blank=True)
    advanced = models.JSONField(default=dict, blank=True, help_text="Lossless catch-all (proto, interface, categories, …).")

    class Meta:
        ordering = ["name"]
        verbose_name = "Firewall Alias"
        verbose_name_plural = "Firewall Aliases"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_pf:alias", args=[self.pk])


class FirewallRule(NetBoxModel):
    """A single pf rule on a device — the full ``<filter><rule>`` shape, lossless.

    Platform-agnostic across **OPNsense and pfSense** (both FreeBSD pf): the common
    fields are explicit columns; platform-specific identifiers (pfSense ``tracker``,
    OPNsense MVC ``uuid``) and the long-tail pf options live in ``advanced`` (JSON), so
    either platform's config round-trips with zero loss. The device's ``platform`` says
    which dialect it came from.
    """
    device = models.ForeignKey(
        "dcim.Device", on_delete=models.CASCADE, related_name="pf_firewall_rules"
    )
    sequence = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], help_text="Evaluation order within the device."
    )
    action = models.CharField(max_length=8, choices=FirewallActionChoices)
    disabled = models.BooleanField(default=False)
    quick = models.BooleanField(default=True, help_text="pf first-match-wins for this rule.")

    # Binding
    interface = models.CharField(
        max_length=512, blank=True, help_text="pf interface(s), comma-separated (raw)."
    )
    floating = models.BooleanField(default=False)
    direction = models.CharField(max_length=4, choices=DirectionChoices, default=DirectionChoices.IN)
    ipprotocol = models.CharField(
        max_length=8, choices=IPProtocolChoices, default=IPProtocolChoices.INET
    )
    protocol = models.CharField(
        max_length=32, blank=True, help_text="tcp/udp/tcp-udp/icmp/esp/…; blank = any."
    )

    # Source (polymorphic pf endpoint)
    source_type = models.CharField(
        max_length=16, choices=EndpointTypeChoices, default=EndpointTypeChoices.ANY
    )
    source = models.CharField(max_length=255, blank=True, help_text="CIDR/host/interface value.")
    source_alias = models.ForeignKey(
        Alias, on_delete=models.PROTECT, null=True, blank=True, related_name="+"
    )
    source_invert = models.BooleanField(default=False)
    source_port = models.CharField(max_length=128, blank=True)

    # Destination (polymorphic pf endpoint)
    destination_type = models.CharField(
        max_length=16, choices=EndpointTypeChoices, default=EndpointTypeChoices.ANY
    )
    destination = models.CharField(max_length=255, blank=True)
    destination_alias = models.ForeignKey(
        Alias, on_delete=models.PROTECT, null=True, blank=True, related_name="+"
    )
    destination_invert = models.BooleanField(default=False)
    destination_port = models.CharField(max_length=128, blank=True)

    # pf-specific advanced fields (the "holes" no foreign ACL model has)
    gateway = models.CharField(max_length=128, blank=True, help_text="Policy-route gateway.")
    log = models.BooleanField(default=False)
    statetype = models.CharField(max_length=32, blank=True)
    sched = models.CharField(max_length=128, blank=True)
    tcpflags = models.CharField(max_length=64, blank=True)
    icmptype = models.CharField(max_length=255, blank=True)
    reply_to = models.CharField(max_length=128, blank=True)
    tag = models.CharField(max_length=128, blank=True, help_text="Tag to set on matching packets.")
    tagged = models.CharField(max_length=128, blank=True, help_text="Match packets already carrying this tag.")
    os = models.CharField(max_length=64, blank=True, help_text="OS fingerprint match.")
    description = models.CharField(max_length=255, blank=True)

    # Platform-specific rule identity (kept verbatim for round-trip)
    tracker = models.CharField(max_length=64, blank=True, help_text="pfSense rule tracker ID.")
    uuid = models.CharField(max_length=64, blank=True, help_text="OPNsense MVC rule UUID.")
    associated_rule_id = models.CharField(max_length=64, blank=True, help_text="Linked NAT/assoc rule id.")
    advanced = models.JSONField(
        default=dict, blank=True,
        help_text="Lossless catch-all for long-tail pf options (max-states, statetimeout, "
                  "tcpflags1/2, sloppy/no-sync state, prio/set-prio, shaper/dnpipe, …).",
    )

    class Meta:
        ordering = ["device", "sequence"]
        unique_together = [["device", "sequence"]]
        verbose_name = "Firewall Rule"

    def __str__(self):
        return f"{self.device}: {self.sequence:04d} {self.action}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_pf:firewallrule", args=[self.pk])

    def get_action_color(self):
        return FirewallActionChoices.colors.get(self.action)


class NATRule(NetBoxModel):
    """A pf NAT rule — port-forward (DNAT), outbound (SNAT), or 1:1 (binat). A single
    polymorphic model over all three pfSense/OPNsense NAT tables; every field is a real
    column and ``advanced`` (JSON) holds the long-tail, so a NAT entry round-trips losslessly.
    """
    device = models.ForeignKey(
        "dcim.Device", on_delete=models.CASCADE, related_name="pf_nat_rules"
    )
    nat_type = models.CharField(max_length=16, choices=NATTypeChoices)
    sequence = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], help_text="Order within the device's NAT table of this type."
    )
    disabled = models.BooleanField(default=False)
    interface = models.CharField(max_length=128, blank=True, help_text="pf interface (raw).")
    ipprotocol = models.CharField(max_length=8, blank=True, help_text="inet/inet6 (port-forward).")
    protocol = models.CharField(max_length=32, blank=True, help_text="tcp/udp/…; blank = any.")

    # Match (original packet)
    source = models.CharField(max_length=255, blank=True)
    source_port = models.CharField(max_length=128, blank=True)
    destination = models.CharField(max_length=255, blank=True)
    destination_port = models.CharField(max_length=128, blank=True)

    # Translation
    target = models.CharField(max_length=255, blank=True, help_text="Translation/redirect target (NAT IP/subnet).")
    local_port = models.CharField(max_length=128, blank=True, help_text="Port-forward redirect (internal) port.")
    target_subnet = models.CharField(max_length=64, blank=True, help_text="Outbound translation subnet bits.")
    external = models.CharField(max_length=255, blank=True, help_text="1:1 external address.")

    # Options
    nat_port = models.CharField(max_length=128, blank=True, help_text="Outbound static NAT port.")
    static_nat_port = models.BooleanField(default=False)
    nonat = models.BooleanField(default=False, help_text="Outbound: do-not-NAT (exclusion) rule.")
    nordr = models.BooleanField(default=False, help_text="Port-forward: no redirect (negate).")
    nosync = models.BooleanField(default=False, help_text="Do not sync to CARP peer.")
    natreflection = models.CharField(max_length=32, blank=True)
    poolopts = models.CharField(max_length=64, blank=True, help_text="Outbound pool option.")
    associated_rule_id = models.CharField(max_length=64, blank=True, help_text="Linked firewall rule (port-forward).")
    description = models.CharField(max_length=255, blank=True)
    advanced = models.JSONField(
        default=dict, blank=True, help_text="Lossless catch-all (source_hash_key, natport ranges, …)."
    )

    class Meta:
        ordering = ["device", "nat_type", "sequence"]
        unique_together = [["device", "nat_type", "sequence"]]
        verbose_name = "NAT Rule"

    def __str__(self):
        return f"{self.device}: {self.nat_type} {self.sequence:04d}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_pf:natrule", args=[self.pk])

    def get_nat_type_color(self):
        return NATTypeChoices.colors.get(self.nat_type)


class Gateway(NetBoxModel):
    """An OPNsense/pfSense gateway (System > Gateways): a named next-hop on an interface, with
    optional health monitoring and multi-WAN weighting/priority. netbox-routing models static
    routes but has no gateway concept; this is the OPNsense gateway surface, lossless."""

    device = models.ForeignKey("dcim.Device", on_delete=models.CASCADE, related_name="pf_gateways")
    name = models.CharField(max_length=64)
    interface = models.CharField(max_length=64, help_text="pf interface the gateway is reached on.")
    address = models.GenericIPAddressField(
        null=True, blank=True, help_text="Gateway IP (blank = dynamic / interface-assigned)."
    )
    ipprotocol = models.CharField(
        max_length=8, choices=IPProtocolChoices, default=IPProtocolChoices.INET
    )
    monitor_ip = models.GenericIPAddressField(
        null=True, blank=True, help_text="Address to probe for health (blank = the gateway IP)."
    )
    weight = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])
    priority = models.PositiveSmallIntegerField(
        default=255, help_text="pf gateway priority; lower is preferred."
    )
    far_gateway = models.BooleanField(default=False, help_text="Gateway is outside the interface subnet.")
    default_gateway = models.BooleanField(default=False, help_text="Use as the system default gateway.")
    disabled = models.BooleanField(default=False)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["device", "name"]
        verbose_name = "Gateway"
        unique_together = [["device", "name"]]

    def __str__(self):
        return f"{self.device}: {self.name}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_pf:gateway", args=[self.pk])


class GatewayGroup(NetBoxModel):
    """A gateway group for multi-WAN failover / load-balancing; members are placed at tiers."""

    device = models.ForeignKey(
        "dcim.Device", on_delete=models.CASCADE, related_name="pf_gateway_groups"
    )
    name = models.CharField(max_length=64)
    trigger = models.CharField(
        max_length=20, choices=GatewayTriggerChoices, default=GatewayTriggerChoices.DOWN
    )
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["device", "name"]
        verbose_name = "Gateway Group"
        unique_together = [["device", "name"]]

    def __str__(self):
        return f"{self.device}: {self.name}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_pf:gatewaygroup", args=[self.pk])


class GatewayGroupMember(NetBoxModel):
    """Membership of a Gateway in a GatewayGroup at a failover tier (1 = primary)."""

    group = models.ForeignKey(GatewayGroup, on_delete=models.CASCADE, related_name="members")
    gateway = models.ForeignKey(Gateway, on_delete=models.PROTECT, related_name="group_memberships")
    tier = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)], help_text="Failover tier; lower is preferred."
    )

    class Meta:
        ordering = ["group", "tier"]
        verbose_name = "Gateway Group Member"
        unique_together = [["group", "gateway"]]

    def __str__(self):
        return f"{self.group.name}: {self.gateway.name} (tier {self.tier})"

    def get_absolute_url(self):
        return reverse("plugins:netbox_pf:gatewaygroup", args=[self.group.pk])
