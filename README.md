<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
# netbox-pf

A NetBox 4.6 plugin: a **native source of truth for firewall rules and aliases on both
OPNsense and pfSense** (FreeBSD pf).

Both platforms share the pf `<filter><rule>` schema; they diverge only on identifiers
(pfSense `tracker`, OPNsense MVC `uuid`) and a long-tail of advanced options. This plugin
holds the common fields as explicit columns and the divergences in `tracker`/`uuid`/
`advanced` (JSON) — so a rule from **either** platform round-trips with zero loss.

## Why

NetBox's existing firewall plugins force pf rules through a foreign schema and lose
data:

- **netbox-security** models Juniper/SRX **zones → policies → filters**. Flat pf rules
  have no zones, and its fixed key set has no slot for `gateway` (policy-route), `quick`,
  direction, state-type, sched, or mixed aliases — all dropped.
- **netbox-acls** models **Cisco extended ACLs**. Closer, but still drops the same
  pf-specifics; you end up bolting ~17 custom fields onto it.

`netbox-pf` models the **exact pf schema**: every `<filter><rule>` field is a real
column, so an OPNsense config round-trips with **zero loss**, and the `ansible-tofu`
opnsense module's `firewall_rules` contract reads it back 1:1.

## Model

- **Alias** — `name`, `type` (host/network/port/url/urljson/geoip/mac/external),
  `content`, `description`. Rules reference aliases by FK; aliases may nest by name.
- **FirewallRule** — `device` + `sequence` + `action` (pass/block/reject) + every pf
  field: interface(s)/floating/direction/ipprotocol/protocol; polymorphic **source** and
  **destination** (`*_type` + value + optional `*_alias` FK + `*_invert` + `*_port`);
  `gateway`, `quick`, `log`, `statetype`, `sched`, `tcpflags`, `icmptype`, `reply_to`,
  `tag`, `disabled`, `description`.

Both inherit `NetBoxModel` (custom fields, tags, change logging, GraphQL, REST API).

## Install

```bash
uv pip install --python /opt/netbox/venv/bin/python netbox-pf   # or: pip install -e .
# add "netbox_pf" to PLUGINS in configuration.py
python manage.py migrate netbox_pf
python manage.py collectstatic --no-input
systemctl restart netbox netbox-rq
```

## Develop / test

Tests run against a **real NetBox test database** (no mocks) via NetBox's Django test
framework. See `CLAUDE.md`.

```bash
python /opt/netbox/app/netbox/manage.py test netbox_pf --keepdb -v2
```

## License

AGPL-3.0-or-later.
