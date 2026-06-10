# netbox-pf — Agent Operating Guide

Adapted from `../server-framework`'s `AGENTS.md` (same engineering + test discipline),
re-targeted from FastAPI to a **NetBox 4.6 Django plugin**.

`netbox-pf` is an **AGPL-3.0** NetBox plugin: a **native source of truth for firewall
rules + aliases on both OPNsense and pfSense** (FreeBSD pf). It models the *exact* pf
schema — zero impedance, zero data loss — unlike the Junos-modeled `netbox-security` or
the Cisco-extended-ACL `netbox-acls`, both of which force pf rules through a foreign
schema and drop gateway/quick/state/aliases. Both platforms share the rule schema and
diverge only on identifiers (pfSense `tracker`, OPNsense MVC `uuid`) + a long-tail of
advanced options, held in `tracker`/`uuid`/`advanced`. The `ansible-tofu` opnsense
module's `firewall_rules` contract reads it back to reconcile the live boxes.

---

## Key Directives / Rules

### DO, ALWAYS:
- If functionality won't work without a parameter, make it a **required positional**
  parameter — never an optional one with an inline presence check.
- Any time you modify a source file, ensure its accompanying test under `tests/`
  contains **comprehensive tests for the change WITHOUT MOCKS**, and update any `.md`
  in the same directory that references the changed code.
- Write concise code (avoid obvious comments; use one-liners where possible).
- Critically analyze requirements and ask all necessary clarifying questions before
  implementing or refactoring.
- Phrase documentation for yourself (AI) and for autistic/ADHD humans: a clear
  architectural summary you could reconstruct the code from with 95% accuracy, with
  minimal snippets — **not** usage examples (the browsable REST/GraphQL schema is the
  usage reference).

### DO NOT, EVER, UNDER ANY CIRCUMSTANCE:
- Make assumptions, or answer with "is likely", "probably", or "might be".
- Use frame-local or thread-local state instead of passing data via parameters.
- Skip a failing test instead of fixing the root cause.
- Fix broken functionality while keeping the broken path as a fallback.
- Re-implement existing functionality in a second location to bypass the original.
- Use bandaid fixes instead of fixing the core functionality.
- **Mock the database, the ORM, the NetBox API test client, or any integration path.**
  Tests run against a **real test database** via NetBox's Django test framework — use
  real model instances and real API requests. Only pure utility functions (e.g. a
  pf-expression parser/normalizer) may use mocks for isolation.

### Python / Django Guidelines:
- Import children of `datetime`: `from datetime import date` — **never** `import
  datetime` then `datetime.date`.
- Imports are package-relative inside `netbox_pf` (`from .models import FirewallRule`),
  never `from netbox_pf.models import ...`.
- Models inherit `netbox.models.NetBoxModel` (custom fields, tags, journaling, change
  logging, GraphQL — for free).
- **SPDX header on every source file**: `# SPDX-License-Identifier: AGPL-3.0-or-later`.

### Documentation Guidelines:
- Markdown docs are concise: reconstruct-the-code-with-95%-accuracy architectural
  summaries with minimal snippets, not usage tutorials.

---

## Architecture (NetBox 4.6 plugin)

| File | Responsibility |
|------|----------------|
| `__init__.py` | `PluginConfig` — name `netbox_pf`, `base_url='pf'`, min/max NetBox version |
| `choices.py` | `ChoiceSet`s: action, direction, ipprotocol, endpoint-type, alias-type |
| `models.py` | `Alias`, `FirewallRule` — the native pf schema (see §Model) |
| `migrations/` | schema migrations — regenerate with `makemigrations netbox_pf` against the target NetBox; never hand-edit generated state |
| `api/serializers.py`, `api/views.py`, `api/urls.py` | REST API (`NetBoxModelViewSet`) — the contract `ansible-tofu` reads |
| `filtersets.py` | `NetBoxModelFilterSet` per model (drives API + UI filtering) |
| `tables.py`, `forms.py`, `navigation.py`, `views.py`, `urls.py`, `templates/` | UI layer |
| `graphql/` | GraphQL types (optional) |

### Model — the pf SoT (lossless by construction)
- **`Alias`**: `name`, `type` (host/network/port/url/urljson/geoip/mac/external),
  `content` (members; may reference other aliases by name), `description`.
- **`FirewallRule`**: `device` FK + `sequence` + `action` (pass/block/reject) + **every
  pf field**: `interface`(s)/`floating`/`direction`/`ipprotocol`/`protocol`; polymorphic
  **source** & **destination** (`*_type` + value + optional `*_alias` FK + `*_invert` +
  `*_port`); `gateway` (policy-route), `quick`, `log`, `statetype`, `sched`, `tcpflags`,
  `icmptype`, `reply_to`, `tag`, `disabled`, `description`. Every pf field is a real
  column → an OPNsense `<filter><rule>` round-trips with **zero loss**.

---

## Testing (NO MOCKS — real DB, NetBox test framework)

- Tests live in `tests/`, one module per source module (`tests/test_models.py`,
  `tests/test_api.py`, `tests/test_filtersets.py`, `tests/test_roundtrip.py`, …).
- Use NetBox's base classes from `utilities.testing`: `ModelViewTestCase` /
  `ViewTestCases`, `APIViewTestCases.APIViewTestCase`, `ChangeLoggedFilterSetTests`.
  They exercise models, API, and filters against a **real test database** — no mocks.
- **Test isolation**: Django wraps each test in a transaction against a per-run test
  database with automatic teardown.
- **Never skip a failing test** — fix the root cause; repair deficiencies starting with
  the lowest-hanging fruit.
- **Run**: `python /opt/netbox/app/netbox/manage.py test netbox_pf --keepdb -v2`
  (or `pytest` with `pytest-django` + `DJANGO_SETTINGS_MODULE=netbox.settings`).
- **Coverage bar**: every model, serializer, filterset, and view has tests; the pf
  round-trip (`<filter><rule>` → `FirewallRule` → `firewall_rules` contract) has an
  end-to-end test that asserts **zero field loss**.

---

## Licensing
- **AGPL-3.0-or-later** (workspace production-IaC standard). SPDX header in every file.
