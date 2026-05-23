# metaphactory-automation — Python Library Design

**Status:** Approved design, pending spec review
**Date:** 2026-05-23
**Author:** kchemorion (with Claude)

## Goal

Turn the battle-tested `mf_helpers.py` automation code into a public,
pip-installable Python library for automating the metaphactory platform. It
combines HTTP access (SPARQL, REST) with Playwright UI automation for the parts
that exist only in the browser, behind one clean object-oriented client — with
the low-level functional helpers exposed as an escape hatch.

## Non-goals

- Not a general RDF/SPARQL toolkit (use rdflib for graph manipulation).
- Not a metaphactory app/template framework — it *drives* metaphactory, it
  doesn't replace its UI.
- v0.1.0 does not aim for full feature coverage (see Scope).

## Distribution & naming

- **PyPI distribution name:** `metaphactory-automation`
- **Import name:** `metaphactory_automation`
- **License:** MIT
- **Versioning:** semver; first release `0.1.0` (pre-1.0 — public API may change
  between minor versions).
- **Trademark:** "metaphactory" is a trademark of metaphacts GmbH. The package
  must NOT claim the bare `metaphactory` name and MUST carry a prominent
  "**Unofficial. Not affiliated with or endorsed by metaphacts GmbH.**"
  disclaimer in the README, docs, and package description.

## Repository layout

The library lives **inside the existing `kchemorion/metaphactory` repo** as a
self-contained package, making the repo a light monorepo (tutorial scripts at
root + published package under `lib/`).

```
metaphactory/                         # existing repo root
├── README.md                         # tutorial + link to the library
├── tutorial.py, v2/, ...             # existing scripts (unchanged)
├── metaphactory-automation/          # the installable skill (existing)
└── lib/
    └── metaphactory-automation/      # THE PYTHON PACKAGE (this design)
        ├── pyproject.toml
        ├── README.md                 # package readme (with disclaimer)
        ├── CHANGELOG.md
        ├── LICENSE                   # MIT
        ├── src/
        │   └── metaphactory_automation/
        │       ├── __init__.py       # exports Metaphactory, errors, version
        │       ├── py.typed
        │       ├── _version.py
        │       ├── errors.py
        │       ├── selectors.py      # versioned selector profiles
        │       ├── models.py         # Vocabulary, Ontology, Concept, SparqlResult
        │       ├── transport/
        │       │   ├── __init__.py
        │       │   ├── auth.py        # form login → session cookie
        │       │   ├── browser.py     # BrowserSession (Playwright lifecycle)
        │       │   └── http.py        # HttpSession (httpx + shared cookie)
        │       ├── helpers/           # Layer 1 — functional escape hatch
        │       │   ├── __init__.py
        │       │   ├── forms.py       # react_type, react_select_pick, create_asset_dialog
        │       │   ├── tree.py        # tree_click_concept, tree_concept_menu, concepts, status
        │       │   ├── ontology.py    # class/attribute/relation, tabs
        │       │   ├── editors.py     # codemirror_*, monaco_set_via_keyboard
        │       │   ├── workflow.py    # git_save, catalog_more_vert, catalog_action
        │       │   └── common.py      # dismiss_modals, navigate, screenshot
        │       ├── client.py          # Layer 2 — Metaphactory facade (sync)
        │       ├── vocabularies.py    # VocabulariesAPI + Vocabulary
        │       ├── ontologies.py      # OntologiesAPI + Ontology
        │       ├── sparql.py          # SparqlAPI (HTTP)
        │       ├── templates.py       # TemplatesAPI (browser/Monaco) [experimental]
        │       ├── services.py        # AI services / QaaS [experimental]
        │       └── aio/               # async variant, generated via unasync
        ├── tests/
        │   ├── unit/                  # no browser, always in CI
        │   └── integration/           # @pytest.mark.integration, live instance
        ├── docs/                      # mkdocs-material
        └── docker-compose.yml         # metaphacts/metaphactory:5.10.0 for tests
```

## Architecture

Three layers, lowest to highest:

### Layer 0 — Transport & auth (`transport/`)

- **`auth.py`** — performs the metaphactory form login (`POST /login` style /
  the existing `input[name=username/password]` flow) **once** and captures the
  session cookie. This single authenticated session is shared by both transports
  below — this is the clean way to keep HTTP and browser in lockstep.
- **`BrowserSession`** (`browser.py`) — owns the Playwright lifecycle
  (playwright start, browser launch, context with verified defaults: 1920×1080,
  clipboard perms, optional video). Injects the shared session cookie into the
  context so the browser is already authenticated. Provides `navigate()` (retry +
  networkidle-timeout tolerance), `screenshot()`, and modal cleanup. Can also
  accept an externally-provided Playwright `page`/`context` for advanced users.
- **`HttpSession`** (`http.py`) — an `httpx` client carrying the same session
  cookie, targeting the SPARQL endpoint and REST APIs. Used for data operations.

Auth flow: log in over HTTP to get the cookie, inject into both the httpx client
and the Playwright context. (Fallback: if HTTP form login proves unreliable on
some deployments, log in via the browser and extract the cookie from the
context — decided during implementation, behind the same `auth` interface.)

### Layer 1 — Functional helpers (`helpers/`)

The current `mf_helpers.py` functions, cleaned, typed, split by concern, and
operating on a Playwright `page`. This is the **escape hatch**: every advanced
or not-yet-wrapped operation is reachable here via `mf.helpers`. These are the
proven primitives the OO layer is built on.

### Layer 2 — OO client (`client.py` + per-domain modules)

`Metaphactory` is the facade and a context manager that owns the transports.
Sub-APIs and their backing transport:

| Namespace | Backing transport | v0.1.0 status |
|-----------|-------------------|---------------|
| `mf.vocabularies` | browser | **stable** |
| `mf.sparql` | HTTP | **stable** |
| `mf.ontologies` | browser | fast-follow |
| `mf.catalog` (editorial/git) | browser | fast-follow |
| `mf.templates` | browser (Monaco) | experimental |
| `mf.services` (AI/QaaS) | browser + HTTP | experimental |
| `mf.helpers` | browser | always available (escape hatch) |

The client routes each operation to the right transport; callers never choose.

## Public API (target shape)

```python
from metaphactory_automation import Metaphactory

with Metaphactory("http://localhost:10214", "admin", "admin", headless=True) as mf:
    voc = mf.vocabularies.create("Vegetables")        # browser
    voc.add_top_concept("Vegetables", definition="...")
    voc.add_narrower("Vegetables", "Carrot")
    voc.set_status("Carrot", "In review")
    voc.commit()                                       # git versioning

    rows = mf.sparql.query("SELECT * WHERE {?s ?p ?o} LIMIT 10")  # HTTP
    mf.sparql.update("INSERT DATA { ... }")                        # HTTP

    mf.helpers.react_type(locator, "text")             # escape hatch
```

Async mirror (generated):

```python
from metaphactory_automation.aio import Metaphactory
async with Metaphactory(...) as mf:
    rows = await mf.sparql.query("...")
```

Construction options: `Metaphactory(base_url, username=None, password=None, *,
headless=True, browser="chromium", selector_profile=None, http_verify=True,
page=None, storage_state=None)`. `username/password` omitted + `storage_state`
or `page` provided supports pre-authenticated/injected sessions.

## Sync + async strategy

Write the **async** implementation as the single source of truth; generate the
**sync** package with `unasync` at build time (the httpx / redis-py pattern).
Ship both: `metaphactory_automation` (sync) and `metaphactory_automation.aio`
(async). No hand-maintained duplication.

## Selector management

All UI selectors live in `selectors.py` as a **versioned profile** object (a
dataclass / mapping). The 5.10.0-verified selectors from the existing skill are
the default profile. `Metaphactory(..., selector_profile=my_profile)` lets users
override individual selectors for other metaphactory versions without forking.
This isolates the single most version-fragile part of the codebase.

## Error handling

Typed exception hierarchy in `errors.py`:

- `MetaphactoryError` (base)
- `LoginError` — auth failed / redirected back to /login
- `IRIConflictError` — asset IRI already exists (ghost data); raised or
  auto-resolved with a unique IRI depending on a `on_iri_conflict` option
- `WorkflowError` — editorial action unavailable in the current state
- `ElementNotReadyError` — wraps a Playwright timeout with operation context
- `SparqlError` — HTTP/SPARQL endpoint errors

The OO layer calls `dismiss_modals` automatically between high-level operations.
`networkidle` waits are always wrapped (timeout-tolerant).

## Testing (TDD)

- **Unit tests** (`tests/unit/`, no browser, run in CI on every PR): IRI
  generation, selector-profile resolution/override, SPARQL JSON result parsing
  into `SparqlResult`, URL building, auth cookie handling (mocked HTTP).
- **Integration tests** (`tests/integration/`, `@pytest.mark.integration`,
  opt-in): run against a live instance from `docker-compose.yml`
  (`metaphacts/metaphactory:5.10.0`), gated on an `MF_URL`/`MF_USER`/`MF_PASS`
  env. Cover the create-vocabulary and SPARQL round-trips for v0.1.0.
- Development follows RED→GREEN→REFACTOR per test-driven-development.

## Tooling & CI

- **Build:** `pyproject.toml` with hatchling, `src/` layout, `py.typed`.
- **Lint/format/type:** ruff + mypy.
- **Tests:** pytest (markers: `integration`).
- **CI (GitHub Actions):** on PR → ruff + mypy + unit tests across Python
  3.10–3.13; nightly / manual dispatch → integration tests with a metaphactory
  service container.
- **Docs:** mkdocs-material (quickstart, API reference, version-profile guide,
  disclaimer).
- **Release:** tag → build → publish to PyPI (trusted publishing); `CHANGELOG.md`
  kept per release.

## v0.1.0 scope (walking skeleton)

Build the **entire layered architecture end-to-end** but wire only two
operations through to working+tested:

- **`mf.vocabularies.create()` + `Vocabulary.add_top_concept()` /
  `.add_narrower()` / `.set_status()` / `.commit()`** (browser path)
- **`mf.sparql.query()` / `.update()`** (HTTP path)

Both fully covered by unit + integration tests, both sync and async, published
as `0.1.0`. This validates: shared-session auth across both transports, the
selector-profile mechanism, the unasync build, packaging, and CI.

**Fast-follow releases:** `0.2.0` ontologies + editorial/git; `0.3.0` templates;
`0.4.0` AI services / QaaS (experimental).

## Risks & mitigations

| Risk | Mitigation |
|------|------------|
| HTTP form-login differs across deployments | `auth` interface abstracts it; browser-cookie-extraction fallback |
| Selector drift across metaphactory versions | versioned `selector_profile`, overridable |
| unasync codegen friction | keep async core small and idiomatic; CI checks sync output is in sync |
| Integration tests flaky/slow in CI | gated + nightly, not on every PR; dockerized fixed version |
| Trademark concerns | distinct package name + prominent disclaimer |
```
