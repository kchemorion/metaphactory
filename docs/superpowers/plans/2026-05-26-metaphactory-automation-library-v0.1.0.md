# metaphactory-automation Python Library — v0.1.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `metaphactory-automation` v0.1.0 to PyPI — a hybrid HTTP+Playwright library whose OO client can create a SKOS vocabulary (browser) and run SPARQL (HTTP), with the full layered architecture, sync+async, typed errors, versioned selectors, tests, and CI in place.

**Architecture:** Three layers. Layer 0 `transport/` owns auth + a Playwright `BrowserSession` and an httpx `HttpSession` that share one login cookie. Layer 1 `helpers/` holds the proven Playwright primitives (escape hatch). Layer 2 is the `Metaphactory` OO facade with `mf.vocabularies` (browser) and `mf.sparql` (HTTP). The async implementation is the single source of truth; the sync package is generated with `unasync` at build time.

**Tech Stack:** Python 3.10–3.13, Playwright (async+sync), httpx, unasync, pytest + pytest-asyncio + respx, ruff, mypy, hatchling, GitHub Actions, mkdocs-material.

**Spec:** `docs/superpowers/specs/2026-05-23-metaphactory-automation-library-design.md`

**Scope:** v0.1.0 walking skeleton ONLY — `mf.vocabularies.create/add_top_concept/add_narrower/set_status/commit` and `mf.sparql.query/update`. Ontologies, editorial-beyond-commit, templates, AI/QaaS are explicitly OUT (fast-follow releases).

**Working directory for all paths below:** `lib/metaphactory-automation/` inside the `kchemorion/metaphactory` repo. "Run:" commands assume `cd lib/metaphactory-automation`.

---

## File Structure

| File | Responsibility |
|------|----------------|
| `pyproject.toml` | Packaging (hatchling), deps, ruff/mypy/pytest config, unasync build hook |
| `LICENSE`, `README.md`, `CHANGELOG.md` | MIT license, package readme w/ trademark disclaimer, changelog |
| `src/metaphactory_automation/__init__.py` | Public exports: `Metaphactory`, errors, `__version__` |
| `src/metaphactory_automation/_version.py` | `__version__ = "0.1.0"` |
| `src/metaphactory_automation/py.typed` | PEP 561 marker (empty file) |
| `src/metaphactory_automation/errors.py` | Exception hierarchy |
| `src/metaphactory_automation/selectors.py` | `SelectorProfile` dataclass + `PROFILE_5_10_0` default |
| `src/metaphactory_automation/models.py` | `SparqlResult`, `Concept` value objects |
| `src/metaphactory_automation/aio/__init__.py` | Async public exports |
| `src/metaphactory_automation/aio/auth.py` | `login_http()` → cookie jar |
| `src/metaphactory_automation/aio/http.py` | `HttpSession` (httpx.AsyncClient + SPARQL) |
| `src/metaphactory_automation/aio/browser.py` | `BrowserSession` (async Playwright) |
| `src/metaphactory_automation/aio/helpers.py` | Async Playwright primitives (escape hatch) |
| `src/metaphactory_automation/aio/sparql.py` | `SparqlAPI` |
| `src/metaphactory_automation/aio/vocabularies.py` | `VocabulariesAPI` + `Vocabulary` |
| `src/metaphactory_automation/aio/client.py` | `Metaphactory` async facade |
| `src/metaphactory_automation/{auth,http,browser,helpers,sparql,vocabularies,client}.py` | **Generated** sync mirror (unasync) — never hand-edited |
| `build_sync.py` | unasync codegen script (also a build hook) |
| `tests/unit/*` | No-browser tests (run every CI) |
| `tests/integration/*` | `@pytest.mark.integration`, live instance |
| `docker-compose.yml` | `metaphacts/metaphactory:5.10.0` for integration |
| `.github/workflows/ci.yml` | lint+type+unit on PR; integration nightly |
| `mkdocs.yml`, `docs/*` | Documentation site |

---

### Task 1: Project scaffold & packaging

**Files:**
- Create: `lib/metaphactory-automation/pyproject.toml`
- Create: `lib/metaphactory-automation/LICENSE`
- Create: `lib/metaphactory-automation/src/metaphactory_automation/__init__.py`
- Create: `lib/metaphactory-automation/src/metaphactory_automation/_version.py`
- Create: `lib/metaphactory-automation/src/metaphactory_automation/py.typed`
- Create: `lib/metaphactory-automation/.gitignore`

- [ ] **Step 1: Create `pyproject.toml`**

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "metaphactory-automation"
dynamic = ["version"]
description = "Unofficial hybrid HTTP + Playwright automation library for the metaphactory platform"
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }
authors = [{ name = "kchemorion" }]
keywords = ["metaphactory", "playwright", "sparql", "knowledge-graph", "automation"]
classifiers = [
  "Development Status :: 3 - Alpha",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  "Programming Language :: Python :: 3.13",
  "License :: OSI Approved :: MIT License",
  "Typing :: Typed",
]
dependencies = [
  "playwright>=1.40",
  "httpx>=0.27",
]

[project.optional-dependencies]
dev = [
  "pytest>=8",
  "pytest-asyncio>=0.23",
  "respx>=0.21",
  "ruff>=0.5",
  "mypy>=1.10",
  "unasync>=0.6",
]

[project.urls]
Homepage = "https://github.com/kchemorion/metaphactory"
Repository = "https://github.com/kchemorion/metaphactory"

[tool.hatch.version]
path = "src/metaphactory_automation/_version.py"

[tool.hatch.build.targets.wheel]
packages = ["src/metaphactory_automation"]

[tool.ruff]
line-length = 100
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.mypy]
python_version = "3.10"
strict = true
files = ["src/metaphactory_automation"]
# Generated sync modules mirror the async source; check the source of truth.
exclude = ['src/metaphactory_automation/(auth|http|browser|helpers|sparql|vocabularies|client)\.py$']

[tool.pytest.ini_options]
asyncio_mode = "auto"
markers = [
  "integration: requires a live metaphactory instance (set MF_URL)",
]
testpaths = ["tests"]
```

- [ ] **Step 2: Create `_version.py` and `py.typed`**

```python
# src/metaphactory_automation/_version.py
__version__ = "0.1.0"
```

`py.typed` is an empty file:

```bash
mkdir -p src/metaphactory_automation
touch src/metaphactory_automation/py.typed
```

- [ ] **Step 3: Create minimal `__init__.py`**

```python
# src/metaphactory_automation/__init__.py
"""Unofficial automation library for the metaphactory platform.

Not affiliated with or endorsed by metaphacts GmbH.
"""
from ._version import __version__

__all__ = ["__version__"]
```

- [ ] **Step 4: Create `LICENSE` (MIT) and `.gitignore`**

```bash
cat > LICENSE <<'EOF'
MIT License

Copyright (c) 2026 kchemorion

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

cat > .gitignore <<'EOF'
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
dist/
build/
*.egg-info/
.venv/
test-results/
EOF
```

- [ ] **Step 5: Install editable and verify import**

Run:
```bash
cd lib/metaphactory-automation
python3 -m pip install -e ".[dev]"
playwright install chromium
python3 -c "import metaphactory_automation as m; print(m.__version__)"
```
Expected: prints `0.1.0`.

- [ ] **Step 6: Commit**

```bash
git add lib/metaphactory-automation
git commit -m "feat(lib): scaffold metaphactory-automation package (pyproject, version, license)"
```

---

### Task 2: Typed error hierarchy

**Files:**
- Create: `src/metaphactory_automation/errors.py`
- Test: `tests/unit/test_errors.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/unit/test_errors.py
import pytest
from metaphactory_automation import errors

def test_all_errors_subclass_base():
    for cls in [errors.LoginError, errors.IRIConflictError,
                errors.WorkflowError, errors.ElementNotReadyError,
                errors.SparqlError]:
        assert issubclass(cls, errors.MetaphactoryError)

def test_iri_conflict_carries_iri():
    e = errors.IRIConflictError("taken", iri="https://x/v1")
    assert e.iri == "https://x/v1"
    assert "taken" in str(e)

def test_base_is_exception():
    assert issubclass(errors.MetaphactoryError, Exception)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_errors.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'metaphactory_automation.errors'`

- [ ] **Step 3: Write `errors.py`**

```python
# src/metaphactory_automation/errors.py
"""Typed exceptions for metaphactory-automation."""
from __future__ import annotations


class MetaphactoryError(Exception):
    """Base class for all library errors."""


class LoginError(MetaphactoryError):
    """Authentication failed or the session was rejected."""


class IRIConflictError(MetaphactoryError):
    """An asset IRI already exists (often ghost data from a deleted asset)."""

    def __init__(self, message: str, *, iri: str | None = None) -> None:
        super().__init__(message)
        self.iri = iri


class WorkflowError(MetaphactoryError):
    """A requested editorial action is not available in the current state."""


class ElementNotReadyError(MetaphactoryError):
    """A UI element was not present/ready in time (wraps a Playwright timeout)."""


class SparqlError(MetaphactoryError):
    """The SPARQL endpoint returned an error or unparseable response."""
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/test_errors.py -v`
Expected: PASS (3 passed)

- [ ] **Step 5: Export errors from package root**

Modify `src/metaphactory_automation/__init__.py`:

```python
# src/metaphactory_automation/__init__.py
"""Unofficial automation library for the metaphactory platform.

Not affiliated with or endorsed by metaphacts GmbH.
"""
from ._version import __version__
from .errors import (
    ElementNotReadyError,
    IRIConflictError,
    LoginError,
    MetaphactoryError,
    SparqlError,
    WorkflowError,
)

__all__ = [
    "__version__",
    "MetaphactoryError",
    "LoginError",
    "IRIConflictError",
    "WorkflowError",
    "ElementNotReadyError",
    "SparqlError",
]
```

- [ ] **Step 6: Commit**

```bash
git add src/metaphactory_automation/errors.py src/metaphactory_automation/__init__.py tests/unit/test_errors.py
git commit -m "feat(lib): typed error hierarchy"
```

---

### Task 3: Versioned selector profile

**Files:**
- Create: `src/metaphactory_automation/selectors.py`
- Test: `tests/unit/test_selectors.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/unit/test_selectors.py
from dataclasses import replace
from metaphactory_automation.selectors import SelectorProfile, PROFILE_5_10_0, default_profile

def test_default_profile_is_5_10_0():
    assert default_profile() is PROFILE_5_10_0
    assert PROFILE_5_10_0.version == "5.10.0"

def test_known_selectors_present():
    p = PROFILE_5_10_0
    assert p.asset_title_input == 'input[data-testid="asset-title-input"]'
    assert "termTree__node" in p.tree_node_ancestor_xpath
    assert p.codemirror == ".CodeMirror"

def test_profile_is_overridable_without_mutation():
    custom = replace(PROFILE_5_10_0, version="6.0.0", codemirror=".cm-editor")
    assert custom.codemirror == ".cm-editor"
    assert PROFILE_5_10_0.codemirror == ".CodeMirror"  # original unchanged
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_selectors.py -v`
Expected: FAIL — `ModuleNotFoundError: ... selectors`

- [ ] **Step 3: Write `selectors.py`**

```python
# src/metaphactory_automation/selectors.py
"""Versioned UI selector profiles. The single most version-fragile part of the
library is isolated here. Override per metaphactory version via
Metaphactory(..., selector_profile=replace(PROFILE_5_10_0, ...))."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SelectorProfile:
    version: str
    # auth / nav
    login_username: str = 'input[name="username"]'
    login_password: str = 'input[name="password"]'
    login_submit: str = 'input[type="submit"]'
    # create-asset dialog
    asset_title_input: str = 'input[data-testid="asset-title-input"]'
    suggest_iri_checkbox: str = 'input[data-testid="suggest-iri-{type}"]'
    suggest_iri_input: str = 'input[data-testid="suggest-iri-{type}-input"]'
    modal_create_button: str = '.modal button:has-text("Create"), [role="dialog"] button:has-text("Create")'
    catalog_create_button: str = 'button:has-text("Create"), a:has-text("Create")'
    # vocabulary tree
    tree_panel: str = '.ontodia-accordion, .termTree, [class*="termTree"]'
    tree_expand_toggle: str = '.LazyTreeSelector--expandToggle, .caret, [class*="expand"]'
    tree_node_ancestor_xpath: str = 'xpath=ancestor::span[contains(@class,"termTree__node")]'
    tree_node_ancestor_xpath_fallback: str = 'xpath=ancestor::div[contains(@class,"LazyTreeSelector--itemContent")]'
    more_vert_button: str = 'button:has-text("more_vert")'
    create_top_concept_button: str = 'button:has-text("Create top-level term")'
    create_narrower_menuitem: str = '.dropdown-menu.show a:has-text("Create narrower term")'
    concept_pref_label: str = 'input[placeholder="Enter preferred label here..."]'
    concept_definition: str = 'textarea[placeholder="Enter definition here..."]'
    concept_submit: str = '.overlay-modal.show button[name="submit"]'
    status_button_tpl: str = '.dropdown-menu.show button.termSetStatusButton:has-text("{status}")'
    # editors
    codemirror: str = ".CodeMirror"
    monaco: str = ".monaco-editor .view-lines, .monaco-editor textarea"
    # git versioning
    more_menu: str = 'button:has-text("More"), [data-testid="more-menu"], button:has-text("more_horiz")'
    git_versioning_item: str = '.dropdown-menu.show a:has-text("Git versioning"), [role="menuitem"]:has-text("Git versioning")'
    git_save_button: str = '.modal.show button:has-text("Save"), .modal.show button:has-text("Commit")'


PROFILE_5_10_0 = SelectorProfile(version="5.10.0")


def default_profile() -> SelectorProfile:
    return PROFILE_5_10_0
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/test_selectors.py -v`
Expected: PASS (3 passed)

- [ ] **Step 5: Commit**

```bash
git add src/metaphactory_automation/selectors.py tests/unit/test_selectors.py
git commit -m "feat(lib): versioned selector profile (5.10.0 default)"
```

---

### Task 4: SPARQL result model

**Files:**
- Create: `src/metaphactory_automation/models.py`
- Test: `tests/unit/test_models.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/unit/test_models.py
from metaphactory_automation.models import SparqlResult

SAMPLE = {
    "head": {"vars": ["s", "label"]},
    "results": {"bindings": [
        {"s": {"type": "uri", "value": "http://ex/1"},
         "label": {"type": "literal", "value": "One"}},
        {"s": {"type": "uri", "value": "http://ex/2"}},  # missing label
    ]},
}

def test_parse_vars_and_rows():
    r = SparqlResult.from_json(SAMPLE)
    assert r.vars == ["s", "label"]
    assert len(r) == 2

def test_rows_are_value_dicts_with_missing_as_none():
    r = SparqlResult.from_json(SAMPLE)
    rows = list(r)
    assert rows[0] == {"s": "http://ex/1", "label": "One"}
    assert rows[1] == {"s": "http://ex/2", "label": None}

def test_ask_result():
    r = SparqlResult.from_json({"head": {}, "boolean": True})
    assert r.boolean is True
    assert len(r) == 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_models.py -v`
Expected: FAIL — `ModuleNotFoundError: ... models`

- [ ] **Step 3: Write `models.py`**

```python
# src/metaphactory_automation/models.py
"""Value objects returned by the API."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator


@dataclass(frozen=True)
class SparqlResult:
    """A parsed SPARQL 1.1 JSON results document.

    Iterating yields one ``dict[str, str | None]`` per row (variable -> value,
    or None if the variable was unbound in that row). For ASK queries, use
    ``.boolean``.
    """

    vars: list[str] = field(default_factory=list)
    rows: list[dict[str, str | None]] = field(default_factory=list)
    boolean: bool | None = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "SparqlResult":
        if "boolean" in data:
            return cls(vars=[], rows=[], boolean=bool(data["boolean"]))
        vars_ = list(data.get("head", {}).get("vars", []))
        rows: list[dict[str, str | None]] = []
        for binding in data.get("results", {}).get("bindings", []):
            row: dict[str, str | None] = {}
            for v in vars_:
                cell = binding.get(v)
                row[v] = cell["value"] if cell is not None else None
            rows.append(row)
        return cls(vars=vars_, rows=rows, boolean=None)

    def __iter__(self) -> Iterator[dict[str, str | None]]:
        return iter(self.rows)

    def __len__(self) -> int:
        return len(self.rows)


@dataclass(frozen=True)
class Concept:
    """A SKOS concept reference (label-based; IRI optional)."""

    label: str
    iri: str | None = None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/test_models.py -v`
Expected: PASS (3 passed)

- [ ] **Step 5: Commit**

```bash
git add src/metaphactory_automation/models.py tests/unit/test_models.py
git commit -m "feat(lib): SparqlResult and Concept models"
```

---

### Task 5: Async auth — HTTP form login → cookie jar

**Files:**
- Create: `src/metaphactory_automation/aio/__init__.py`
- Create: `src/metaphactory_automation/aio/auth.py`
- Test: `tests/unit/test_auth.py`

- [ ] **Step 1: Create empty async package init**

```python
# src/metaphactory_automation/aio/__init__.py
"""Async implementation (single source of truth; sync is generated)."""
```

- [ ] **Step 2: Write the failing test (respx-mocked login)**

```python
# tests/unit/test_auth.py
import httpx
import pytest
import respx
from metaphactory_automation.aio.auth import login_http
from metaphactory_automation.errors import LoginError

BASE = "http://mf.test"

@respx.mock
async def test_login_returns_cookies_on_success():
    route = respx.post(f"{BASE}/login").mock(
        return_value=httpx.Response(302, headers={
            "location": "/resource/Start",
            "set-cookie": "JSESSIONID=abc123; Path=/",
        })
    )
    async with httpx.AsyncClient(base_url=BASE) as client:
        cookies = await login_http(client, "admin", "admin")
    assert route.called
    assert cookies.get("JSESSIONID") == "abc123"

@respx.mock
async def test_login_raises_when_no_session_cookie():
    # metaphactory re-renders the login form (200) on bad creds, no session set
    respx.post(f"{BASE}/login").mock(return_value=httpx.Response(200, text="<form>login</form>"))
    async with httpx.AsyncClient(base_url=BASE) as client:
        with pytest.raises(LoginError):
            await login_http(client, "admin", "wrong")
```

- [ ] **Step 3: Run test to verify it fails**

Run: `pytest tests/unit/test_auth.py -v`
Expected: FAIL — `ModuleNotFoundError: ... aio.auth`

- [ ] **Step 4: Write `aio/auth.py`**

```python
# src/metaphactory_automation/aio/auth.py
"""HTTP form login. metaphactory uses Apache Shiro form auth: POSTing
username/password sets a session cookie used for both HTTP and the browser.

If a deployment does not accept this POST (custom auth), callers fall back to
browser login + cookie extraction (see BrowserSession.login)."""
from __future__ import annotations

import httpx

from ..errors import LoginError

# Cookie names metaphactory / its servlet container may use for the session.
_SESSION_COOKIE_NAMES = ("JSESSIONID", "rememberMe", "metaphactory-session")


async def login_http(client: httpx.AsyncClient, username: str, password: str) -> httpx.Cookies:
    """POST credentials to /login and return the resulting cookie jar.

    Raises LoginError if no recognizable session cookie comes back.
    """
    resp = await client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=False,
    )
    cookies = client.cookies
    if not any(cookies.get(name) for name in _SESSION_COOKIE_NAMES):
        # Some configs set an opaque cookie; accept any cookie on a redirect.
        if resp.status_code in (301, 302, 303) and len(list(cookies.jar)) > 0:
            return cookies
        raise LoginError(
            f"Login failed for user {username!r}: no session cookie set "
            f"(status {resp.status_code})."
        )
    return cookies
```

- [ ] **Step 5: Run test to verify it passes**

Run: `pytest tests/unit/test_auth.py -v`
Expected: PASS (2 passed)

- [ ] **Step 6: Commit**

```bash
git add src/metaphactory_automation/aio/__init__.py src/metaphactory_automation/aio/auth.py tests/unit/test_auth.py
git commit -m "feat(lib): async HTTP form login"
```

---

### Task 6: Async HttpSession + SPARQL transport

**Files:**
- Create: `src/metaphactory_automation/aio/http.py`
- Test: `tests/unit/test_http.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/unit/test_http.py
import httpx
import respx
from metaphactory_automation.aio.http import HttpSession

BASE = "http://mf.test"
SELECT_JSON = {"head": {"vars": ["s"]},
               "results": {"bindings": [{"s": {"type": "uri", "value": "http://ex/1"}}]}}

@respx.mock
async def test_query_parses_results():
    respx.get(f"{BASE}/sparql").mock(return_value=httpx.Response(200, json=SELECT_JSON))
    async with HttpSession(BASE) as s:
        result = await s.query("SELECT * WHERE {?s ?p ?o} LIMIT 1")
    assert result.vars == ["s"]
    assert list(result)[0]["s"] == "http://ex/1"

@respx.mock
async def test_update_posts_update_param():
    route = respx.post(f"{BASE}/sparql").mock(return_value=httpx.Response(200, text=""))
    async with HttpSession(BASE) as s:
        await s.update("INSERT DATA { <http://ex/a> <http://ex/b> <http://ex/c> }")
    assert route.called
    assert b"update=" in route.calls.last.request.content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_http.py -v`
Expected: FAIL — `ModuleNotFoundError: ... aio.http`

- [ ] **Step 3: Write `aio/http.py`**

```python
# src/metaphactory_automation/aio/http.py
"""HTTP transport: an httpx.AsyncClient carrying the shared session cookie,
used for SPARQL query/update over the SPARQL 1.1 protocol."""
from __future__ import annotations

from types import TracebackType
from typing import Any

import httpx

from ..errors import SparqlError
from ..models import SparqlResult
from .auth import login_http


class HttpSession:
    """Authenticated HTTP access to a metaphactory instance.

    Construct with credentials to log in on enter, or pass an existing
    ``cookies`` jar (shared with the browser session).
    """

    def __init__(
        self,
        base_url: str,
        username: str | None = None,
        password: str | None = None,
        *,
        cookies: httpx.Cookies | None = None,
        verify: bool = True,
        sparql_path: str = "/sparql",
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._username = username
        self._password = password
        self._sparql_path = sparql_path
        self._client = httpx.AsyncClient(
            base_url=self._base_url, verify=verify, follow_redirects=True, timeout=60
        )
        if cookies is not None:
            self._client.cookies = cookies

    @property
    def cookies(self) -> httpx.Cookies:
        return self._client.cookies

    async def __aenter__(self) -> "HttpSession":
        if self._username is not None and self._password is not None and not list(self.cookies.jar):
            await login_http(self._client, self._username, self._password)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self._client.aclose()

    async def query(self, sparql: str) -> SparqlResult:
        resp = await self._client.get(
            self._sparql_path,
            params={"query": sparql},
            headers={"Accept": "application/sparql-results+json"},
        )
        if resp.status_code >= 400:
            raise SparqlError(f"SPARQL query failed ({resp.status_code}): {resp.text[:300]}")
        try:
            data: dict[str, Any] = resp.json()
        except ValueError as e:
            raise SparqlError(f"Non-JSON SPARQL response: {resp.text[:300]}") from e
        return SparqlResult.from_json(data)

    async def update(self, sparql: str) -> None:
        resp = await self._client.post(
            self._sparql_path,
            data={"update": sparql},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if resp.status_code >= 400:
            raise SparqlError(f"SPARQL update failed ({resp.status_code}): {resp.text[:300]}")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/test_http.py -v`
Expected: PASS (2 passed)

- [ ] **Step 5: Commit**

```bash
git add src/metaphactory_automation/aio/http.py tests/unit/test_http.py
git commit -m "feat(lib): async HttpSession with SPARQL query/update"
```

---

### Task 7: Async BrowserSession (Playwright lifecycle)

**Files:**
- Create: `src/metaphactory_automation/aio/browser.py`
- Test: `tests/unit/test_browser_unit.py`

This wraps Playwright; behavior is covered by integration tests (Task 12). Unit tests cover only pure logic (URL building, option defaults) using a fake page.

- [ ] **Step 1: Write the failing test**

```python
# tests/unit/test_browser_unit.py
from metaphactory_automation.aio.browser import BrowserSession

def test_resource_url_builds_correctly():
    s = BrowserSession("http://mf.test/")
    assert s.resource_url("Assets:Vocabularies") == "http://mf.test/resource/Assets:Vocabularies"

def test_full_url_passthrough_for_absolute():
    s = BrowserSession("http://mf.test")
    assert s.url("/sparql") == "http://mf.test/sparql"
    assert s.url("http://other/x") == "http://other/x"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_browser_unit.py -v`
Expected: FAIL — `ModuleNotFoundError: ... aio.browser`

- [ ] **Step 3: Write `aio/browser.py`**

```python
# src/metaphactory_automation/aio/browser.py
"""Browser transport: owns the async Playwright lifecycle and provides resilient
navigation + modal cleanup. Shares the session cookie with HttpSession."""
from __future__ import annotations

import asyncio
from types import TracebackType

import httpx
from playwright.async_api import Browser, BrowserContext, Page, async_playwright

from ..selectors import SelectorProfile, default_profile

SLOW = 0.3


class BrowserSession:
    def __init__(
        self,
        base_url: str,
        *,
        headless: bool = True,
        browser_name: str = "chromium",
        selectors: SelectorProfile | None = None,
        record_video_dir: str | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._headless = headless
        self._browser_name = browser_name
        self.selectors = selectors or default_profile()
        self._record_video_dir = record_video_dir
        self._pw = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self.page: Page | None = None

    # --- URL helpers (pure; unit-tested) ---
    def url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self._base_url}/{path.lstrip('/')}"

    def resource_url(self, resource_id: str) -> str:
        return f"{self._base_url}/resource/{resource_id}"

    # --- lifecycle ---
    async def start(self) -> None:
        self._pw = await async_playwright().start()
        launcher = getattr(self._pw, self._browser_name)
        self._browser = await launcher.launch(headless=self._headless, slow_mo=120)
        self._context = await self._browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=self._record_video_dir,
        )
        await self._context.grant_permissions(["clipboard-read", "clipboard-write"])
        self.page = await self._context.new_page()
        self.page.set_default_timeout(15000)

    async def login(self, username: str, password: str) -> httpx.Cookies:
        """Form login via the browser; returns the cookie jar (for HttpSession)."""
        assert self.page is not None
        s = self.selectors
        await self.page.goto(self.url("/login"), wait_until="domcontentloaded")
        await self.page.fill(s.login_username, username)
        await self.page.fill(s.login_password, password)
        await self.page.click(s.login_submit)
        await self.page.wait_for_timeout(3000)
        if "/login" in self.page.url:
            from ..errors import LoginError
            raise LoginError(f"Browser login failed for {username!r}")
        jar = httpx.Cookies()
        for c in await self._context.cookies():
            jar.set(c["name"], c["value"])
        return jar

    async def set_cookies(self, cookies: httpx.Cookies) -> None:
        """Inject an externally-obtained cookie jar into the browser context."""
        assert self._context is not None
        from urllib.parse import urlparse
        host = urlparse(self._base_url).hostname or "localhost"
        await self._context.add_cookies(
            [{"name": k, "value": v, "domain": host, "path": "/"} for k, v in cookies.items()]
        )

    async def navigate(self, path: str, retries: int = 2) -> None:
        assert self.page is not None
        target = self.url(path)
        for attempt in range(retries + 1):
            try:
                await self.page.goto(target, wait_until="domcontentloaded", timeout=30000)
                try:
                    await self.page.wait_for_load_state("networkidle", timeout=10000)
                except Exception:
                    pass  # networkidle rarely settles; page is usable
                await asyncio.sleep(SLOW)
                return
            except Exception:
                if attempt < retries:
                    await asyncio.sleep(2)
                    continue
                return

    async def dismiss_modals(self) -> None:
        assert self.page is not None
        try:
            await self.page.evaluate(
                "document.querySelectorAll('.dropdown-menu.show')"
                ".forEach(m => m.classList.remove('show'));"
            )
        except Exception:
            pass
        for _ in range(3):
            try:
                modal = self.page.locator(".modal.show, .overlay-modal.show")
                if await modal.is_visible(timeout=300):
                    close = modal.locator('.btn-close, button:has-text("Close"), button:has-text("Cancel")').first
                    if await close.is_visible(timeout=300):
                        await close.click(force=True)
                    else:
                        await self.page.keyboard.press("Escape")
                    await asyncio.sleep(SLOW)
                else:
                    break
            except Exception:
                await self.page.keyboard.press("Escape")
                await asyncio.sleep(SLOW)
        try:
            await self.page.evaluate(
                "document.querySelectorAll('.modal-backdrop').forEach(b => b.remove());"
                "document.body.classList.remove('modal-open');"
            )
        except Exception:
            pass

    async def close(self) -> None:
        if self._context is not None:
            await self._context.close()
        if self._browser is not None:
            await self._browser.close()
        if self._pw is not None:
            await self._pw.stop()

    async def __aenter__(self) -> "BrowserSession":
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.close()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/test_browser_unit.py -v`
Expected: PASS (2 passed)

- [ ] **Step 5: Commit**

```bash
git add src/metaphactory_automation/aio/browser.py tests/unit/test_browser_unit.py
git commit -m "feat(lib): async BrowserSession (lifecycle, navigate, modal cleanup, cookie share)"
```

---

### Task 8: Async Playwright helpers (escape hatch + vocabulary primitives)

**Files:**
- Create: `src/metaphactory_automation/aio/helpers.py`
- Test: `tests/unit/test_helpers_unit.py`

Port the proven, verified primitives from `metaphactory-automation/mf_helpers.py` to async, parameterized by a `SelectorProfile`. v0.1.0 needs only the vocabulary path. Behavior is integration-tested (Task 12); the unit test here covers the pure `unique_iri` helper.

- [ ] **Step 1: Write the failing test**

```python
# tests/unit/test_helpers_unit.py
import re
from metaphactory_automation.aio.helpers import unique_iri

def test_unique_iri_appends_timestamp_and_strips_trailing():
    out = unique_iri("https://vocabularies.metaphacts.com/veg/#")
    assert out.startswith("https://vocabularies.metaphacts.com/veg")
    assert re.search(r"_\d{14}$", out)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_helpers_unit.py -v`
Expected: FAIL — `ModuleNotFoundError: ... aio.helpers`

- [ ] **Step 3: Write `aio/helpers.py`**

```python
# src/metaphactory_automation/aio/helpers.py
"""Async Playwright primitives. These are the escape hatch and the building
blocks the OO layer composes. Verified against metaphactory 5.10.0.

Each function takes a Playwright async `page` and a SelectorProfile so the
selectors stay overridable per version."""
from __future__ import annotations

import asyncio
from datetime import datetime

from playwright.async_api import Locator, Page

from ..selectors import SelectorProfile

SLOW = 0.3


def unique_iri(base: str) -> str:
    """Timestamped IRI to dodge 'already exists' conflicts from ghost data."""
    return f"{base.rstrip('/#')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"


async def react_type(locator: Locator, text: str, delay: int = 30) -> None:
    """Type char-by-char so React's onChange fires. fill() does NOT update React
    state; never fill('') a React input first."""
    await locator.click()
    await asyncio.sleep(0.1)
    await locator.type(text, delay=delay)
    await asyncio.sleep(0.5)


async def create_asset_dialog(
    page: Page, sel: SelectorProfile, title: str, asset_type: str = "vocabulary"
) -> None:
    """Fill the open Create Vocabulary/Ontology dialog and click Create,
    falling back to a unique IRI on conflict."""
    title_input = page.locator(sel.asset_title_input).first
    await title_input.wait_for(state="visible", timeout=5000)
    await react_type(title_input, title)
    await asyncio.sleep(1)
    create_btn = page.locator(sel.modal_create_button).first
    await asyncio.sleep(1)
    if await create_btn.get_attribute("disabled") is not None:
        cb = page.locator(sel.suggest_iri_checkbox.format(type=asset_type)).first
        if await cb.is_visible(timeout=1000) and await cb.is_checked():
            await cb.click()
            await asyncio.sleep(0.5)
        iri_input = page.locator(sel.suggest_iri_input.format(type=asset_type)).first
        if await iri_input.is_visible(timeout=2000):
            host = "ontologies" if asset_type == "ontology" else "vocabularies"
            base = f"https://{host}.metaphacts.com/{title.lower().replace(' ', '-')}"
            await react_type(iri_input, unique_iri(base) + "/0.1")
            await asyncio.sleep(0.5)
    for _ in range(30):
        if await create_btn.get_attribute("disabled") is None:
            break
        await asyncio.sleep(0.3)
    await create_btn.click()
    await asyncio.sleep(3)


async def tree_click_concept(page: Page, sel: SelectorProfile, label: str) -> Locator:
    """Click a concept in the tree, expanding collapsed parents."""
    tree = page.locator(sel.tree_panel).first
    node = tree.locator(f'a:has-text("{label}")').first
    if not await node.is_visible(timeout=2000):
        toggles = tree.locator(sel.tree_expand_toggle)
        for i in range(await toggles.count()):
            t = toggles.nth(i)
            if await t.is_visible():
                await t.click()
                await asyncio.sleep(0.3)
                if await node.is_visible():
                    break
        node = tree.locator(f'a:has-text("{label}")').first
    await node.click(force=True)
    await asyncio.sleep(1)
    return node


async def tree_concept_menu(page: Page, sel: SelectorProfile, label: str) -> None:
    """Open the more_vert menu for a SPECIFIC concept (never the global .first)."""
    node = await tree_click_concept(page, sel, label)
    container = node.locator(sel.tree_node_ancestor_xpath).first
    menu_btn = container.locator(sel.more_vert_button).first
    if not await menu_btn.is_visible(timeout=1500):
        container = node.locator(sel.tree_node_ancestor_xpath_fallback).first
        menu_btn = container.locator(sel.more_vert_button).first
    await menu_btn.wait_for(state="visible", timeout=3000)
    await menu_btn.click()
    await asyncio.sleep(0.5)


async def _fill_concept_form(page: Page, sel: SelectorProfile, label: str, definition: str) -> None:
    pref = page.locator(sel.concept_pref_label).first
    await pref.wait_for(state="visible", timeout=5000)
    await pref.click()
    await pref.type(label, delay=30)
    await asyncio.sleep(0.5)
    if definition:
        d = page.locator(sel.concept_definition).first
        if await d.is_visible(timeout=1000):
            await d.click()
            await d.type(definition, delay=20)
    save = page.locator(sel.concept_submit).first
    await save.wait_for(state="visible", timeout=3000)
    await asyncio.sleep(0.3)
    await save.click()
    await asyncio.sleep(1.5)


async def create_top_concept(page: Page, sel: SelectorProfile, label: str, definition: str = "") -> None:
    await page.locator(sel.create_top_concept_button).first.click()
    await asyncio.sleep(1.5)
    await _fill_concept_form(page, sel, label, definition)


async def create_narrower_concept(
    page: Page, sel: SelectorProfile, parent: str, child: str, definition: str = ""
) -> None:
    await tree_concept_menu(page, sel, parent)
    await page.locator(sel.create_narrower_menuitem).first.click()
    await asyncio.sleep(1)
    await _fill_concept_form(page, sel, child, definition)


async def set_concept_status(page: Page, sel: SelectorProfile, label: str, status: str) -> None:
    await tree_concept_menu(page, sel, label)
    btn = page.locator(sel.status_button_tpl.format(status=status)).first
    if await btn.is_visible(timeout=2000):
        await btn.click()
        await asyncio.sleep(1)
        confirm = page.locator('button:has-text("Confirm"), button:has-text("Yes")')
        if await confirm.count() > 0 and await confirm.first.is_visible(timeout=800):
            await confirm.first.click()
            await asyncio.sleep(0.5)


async def git_save(page: Page, sel: SelectorProfile) -> None:
    """Save via More > Git versioning > Save. Caller must dismiss_modals after."""
    more = page.locator(sel.more_menu).first
    if not await more.is_visible(timeout=3000):
        return
    await more.click()
    await asyncio.sleep(0.5)
    git = page.locator(sel.git_versioning_item).first
    if not await git.is_visible(timeout=2000):
        return
    await git.click()
    await asyncio.sleep(2)
    save = page.locator(sel.git_save_button).first
    if await save.is_visible(timeout=3000):
        await save.click()
        await asyncio.sleep(2)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/test_helpers_unit.py -v`
Expected: PASS (1 passed)

- [ ] **Step 5: Commit**

```bash
git add src/metaphactory_automation/aio/helpers.py tests/unit/test_helpers_unit.py
git commit -m "feat(lib): async Playwright helpers (vocabulary primitives)"
```

---

### Task 9: Async SparqlAPI

**Files:**
- Create: `src/metaphactory_automation/aio/sparql.py`
- Test: `tests/unit/test_sparql_api.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/unit/test_sparql_api.py
import httpx
import respx
from metaphactory_automation.aio.http import HttpSession
from metaphactory_automation.aio.sparql import SparqlAPI

BASE = "http://mf.test"

@respx.mock
async def test_sparql_api_query_delegates_to_session():
    respx.get(f"{BASE}/sparql").mock(return_value=httpx.Response(
        200, json={"head": {"vars": ["x"]}, "results": {"bindings": [{"x": {"value": "1"}}]}}))
    async with HttpSession(BASE) as s:
        api = SparqlAPI(s)
        r = await api.query("SELECT ?x WHERE {?x ?p ?o}")
    assert list(r)[0]["x"] == "1"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_sparql_api.py -v`
Expected: FAIL — `ModuleNotFoundError: ... aio.sparql`

- [ ] **Step 3: Write `aio/sparql.py`**

```python
# src/metaphactory_automation/aio/sparql.py
"""High-level SPARQL API (HTTP transport)."""
from __future__ import annotations

from ..models import SparqlResult
from .http import HttpSession


class SparqlAPI:
    def __init__(self, http: HttpSession) -> None:
        self._http = http

    async def query(self, sparql: str) -> SparqlResult:
        """Run a SELECT/ASK/CONSTRUCT query and return parsed results."""
        return await self._http.query(sparql)

    async def update(self, sparql: str) -> None:
        """Run a SPARQL UPDATE (INSERT/DELETE)."""
        await self._http.update(sparql)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/test_sparql_api.py -v`
Expected: PASS (1 passed)

- [ ] **Step 5: Commit**

```bash
git add src/metaphactory_automation/aio/sparql.py tests/unit/test_sparql_api.py
git commit -m "feat(lib): async SparqlAPI"
```

---

### Task 10: Async VocabulariesAPI + Vocabulary

**Files:**
- Create: `src/metaphactory_automation/aio/vocabularies.py`
- Test: `tests/unit/test_vocabularies_unit.py`

The `Vocabulary` object holds a `BrowserSession` and drives the editor via the helpers. Unit test covers construction/title; real behavior is integration-tested (Task 12).

- [ ] **Step 1: Write the failing test**

```python
# tests/unit/test_vocabularies_unit.py
from metaphactory_automation.aio.vocabularies import Vocabulary

class _FakeBrowser:
    selectors = None

def test_vocabulary_exposes_title():
    v = Vocabulary(_FakeBrowser(), "Vegetables")
    assert v.title == "Vegetables"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_vocabularies_unit.py -v`
Expected: FAIL — `ModuleNotFoundError: ... aio.vocabularies`

- [ ] **Step 3: Write `aio/vocabularies.py`**

```python
# src/metaphactory_automation/aio/vocabularies.py
"""Vocabulary (SKOS) operations via the browser editor."""
from __future__ import annotations

from . import helpers as H
from .browser import BrowserSession


class Vocabulary:
    """Handle to an open vocabulary editor."""

    def __init__(self, browser: BrowserSession, title: str) -> None:
        self._b = browser
        self.title = title

    async def add_top_concept(self, label: str, definition: str = "") -> "Vocabulary":
        await H.create_top_concept(self._b.page, self._b.selectors, label, definition)
        await self._b.dismiss_modals()
        return self

    async def add_narrower(self, parent: str, child: str, definition: str = "") -> "Vocabulary":
        await H.create_narrower_concept(self._b.page, self._b.selectors, parent, child, definition)
        await self._b.dismiss_modals()
        return self

    async def set_status(self, label: str, status: str) -> "Vocabulary":
        await H.set_concept_status(self._b.page, self._b.selectors, label, status)
        await self._b.dismiss_modals()
        return self

    async def commit(self) -> "Vocabulary":
        """Save to git versioning."""
        await H.git_save(self._b.page, self._b.selectors)
        await self._b.dismiss_modals()
        return self


class VocabulariesAPI:
    def __init__(self, browser: BrowserSession) -> None:
        self._b = browser

    async def create(self, title: str) -> Vocabulary:
        """Create a new vocabulary and return a handle to its editor."""
        await self._b.navigate("/resource/Assets:Vocabularies")
        await self._b.dismiss_modals()
        await self._b.page.locator(self._b.selectors.catalog_create_button).first.click()
        await self._b.page.wait_for_timeout(1000)
        await H.create_asset_dialog(self._b.page, self._b.selectors, title, asset_type="vocabulary")
        await self._b.dismiss_modals()
        return Vocabulary(self._b, title)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/unit/test_vocabularies_unit.py -v`
Expected: PASS (1 passed)

- [ ] **Step 5: Commit**

```bash
git add src/metaphactory_automation/aio/vocabularies.py tests/unit/test_vocabularies_unit.py
git commit -m "feat(lib): async VocabulariesAPI and Vocabulary"
```

---

### Task 11: Async Metaphactory facade (client)

**Files:**
- Create: `src/metaphactory_automation/aio/client.py`
- Modify: `src/metaphactory_automation/aio/__init__.py`
- Test: `tests/unit/test_client_unit.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/unit/test_client_unit.py
from metaphactory_automation.aio.client import Metaphactory
from metaphactory_automation.selectors import PROFILE_5_10_0

def test_client_stores_config_and_default_profile():
    mf = Metaphactory("http://mf.test/", "admin", "admin")
    assert mf._base_url == "http://mf.test"
    assert mf._selectors is PROFILE_5_10_0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/unit/test_client_unit.py -v`
Expected: FAIL — `ModuleNotFoundError: ... aio.client`

- [ ] **Step 3: Write `aio/client.py`**

```python
# src/metaphactory_automation/aio/client.py
"""The Metaphactory async facade. Owns both transports (sharing one login
cookie) and exposes the OO sub-APIs."""
from __future__ import annotations

from types import TracebackType

from ..selectors import SelectorProfile, default_profile
from .browser import BrowserSession
from .helpers import unique_iri  # noqa: F401  (re-exported convenience)
from .http import HttpSession
from .sparql import SparqlAPI
from .vocabularies import VocabulariesAPI


class Metaphactory:
    def __init__(
        self,
        base_url: str,
        username: str | None = None,
        password: str | None = None,
        *,
        headless: bool = True,
        browser: str = "chromium",
        selector_profile: SelectorProfile | None = None,
        http_verify: bool = True,
        record_video_dir: str | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._username = username
        self._password = password
        self._selectors = selector_profile or default_profile()
        self._browser_session = BrowserSession(
            self._base_url,
            headless=headless,
            browser_name=browser,
            selectors=self._selectors,
            record_video_dir=record_video_dir,
        )
        self._http_verify = http_verify
        self._http: HttpSession | None = None
        # sub-APIs (wired on enter)
        self.vocabularies: VocabulariesAPI | None = None
        self.sparql: SparqlAPI | None = None

    @property
    def helpers(self):  # type: ignore[no-untyped-def]
        """Escape hatch: the functional helper module (call with mf.page)."""
        from . import helpers
        return helpers

    @property
    def page(self):  # type: ignore[no-untyped-def]
        return self._browser_session.page

    async def __aenter__(self) -> "Metaphactory":
        await self._browser_session.start()
        # Single login via the browser; share the cookie with HTTP.
        cookies = await self._browser_session.login(self._username or "", self._password or "")
        self._http = HttpSession(self._base_url, cookies=cookies, verify=self._http_verify)
        await self._http.__aenter__()
        self.vocabularies = VocabulariesAPI(self._browser_session)
        self.sparql = SparqlAPI(self._http)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if self._http is not None:
            await self._http.__aexit__(exc_type, exc, tb)
        await self._browser_session.close()
```

- [ ] **Step 4: Export from async package init**

Replace `src/metaphactory_automation/aio/__init__.py`:

```python
# src/metaphactory_automation/aio/__init__.py
"""Async implementation (single source of truth; sync is generated)."""
from .client import Metaphactory

__all__ = ["Metaphactory"]
```

- [ ] **Step 5: Run test to verify it passes**

Run: `pytest tests/unit/test_client_unit.py -v`
Expected: PASS (1 passed)

- [ ] **Step 6: Run full unit suite + mypy + ruff**

Run:
```bash
pytest tests/unit -v
mypy
ruff check .
```
Expected: all unit tests pass; mypy clean; ruff clean.

- [ ] **Step 7: Commit**

```bash
git add src/metaphactory_automation/aio/client.py src/metaphactory_automation/aio/__init__.py tests/unit/test_client_unit.py
git commit -m "feat(lib): async Metaphactory facade (shared-cookie transports)"
```

---

### Task 12: Generate the sync package with unasync

**Files:**
- Create: `build_sync.py`
- Modify: `pyproject.toml` (build hook)
- Modify: `src/metaphactory_automation/__init__.py` (export sync `Metaphactory`)
- Test: `tests/unit/test_sync_generated.py`

- [ ] **Step 1: Write `build_sync.py`**

```python
# build_sync.py
"""Generate the synchronous package from the async source via unasync.

Async source: src/metaphactory_automation/aio/*.py
Sync output : src/metaphactory_automation/*.py  (same leaf names)
Run: python build_sync.py
"""
from __future__ import annotations

import pathlib

import unasync

ROOT = pathlib.Path(__file__).parent
ASYNC_DIR = ROOT / "src" / "metaphactory_automation" / "aio"
SYNC_DIR = ROOT / "src" / "metaphactory_automation"

ADDITIONAL_REPLACEMENTS = {
    # playwright async -> sync
    "async_api": "sync_api",
    "async_playwright": "sync_playwright",
    # httpx async -> sync
    "AsyncClient": "Client",
    "aclose": "close",
    # local: drop the aio subpackage in imports so sync modules import siblings
    "metaphactory_automation.aio": "metaphactory_automation",
    # asyncio.sleep -> time.sleep handled below via import rewrite
    "asyncio": "time",
}

SYNC_MODULES = ["auth", "http", "browser", "helpers", "sparql", "vocabularies", "client"]


def main() -> None:
    rules = [
        unasync.Rule(
            fromdir=str(ASYNC_DIR),
            todir=str(SYNC_DIR),
            additional_replacements=ADDITIONAL_REPLACEMENTS,
        )
    ]
    files = [str(ASYNC_DIR / f"{m}.py") for m in SYNC_MODULES]
    unasync.unasync_files(files, rules)
    # Post-process: asyncio.sleep -> time.sleep (token replacement leaves "time.sleep")
    # and ensure `import time` is present where `import asyncio` was.
    for m in SYNC_MODULES:
        path = SYNC_DIR / f"{m}.py"
        text = path.read_text()
        text = text.replace("import time\n", "import time\n")  # idempotent guard
        text = text.replace("await ", "")
        text = "# AUTO-GENERATED from aio/ by build_sync.py — DO NOT EDIT.\n" + text
        path.write_text(text)


if __name__ == "__main__":
    main()
```

Note: `unasync` already strips `await` and rewrites `async def`→`def`,
`__aenter__`→`__enter__`, `async with`→`with`. The explicit `await ` strip above
is a defensive no-op guard for any missed cases; verify the generated output
imports and runs in Step 5.

- [ ] **Step 2: Write the failing test**

```python
# tests/unit/test_sync_generated.py
def test_sync_client_importable_and_constructs():
    from metaphactory_automation import Metaphactory  # sync, generated
    mf = Metaphactory("http://mf.test", "admin", "admin")
    assert mf._base_url == "http://mf.test"

def test_sync_sparql_query_is_not_coroutine():
    import inspect
    from metaphactory_automation.sparql import SparqlAPI
    assert not inspect.iscoroutinefunction(SparqlAPI.query)
```

- [ ] **Step 3: Run test to verify it fails**

Run: `pytest tests/unit/test_sync_generated.py -v`
Expected: FAIL — `ImportError: cannot import name 'Metaphactory' from 'metaphactory_automation'` (sync modules not generated yet)

- [ ] **Step 4: Generate sync modules**

Run:
```bash
python build_sync.py
ls src/metaphactory_automation/*.py
```
Expected: `auth.py http.py browser.py helpers.py sparql.py vocabularies.py client.py` now exist (plus errors/models/selectors/__init__/_version).

- [ ] **Step 5: Export sync `Metaphactory` and verify generation is sound**

Modify `src/metaphactory_automation/__init__.py` to add:

```python
from .client import Metaphactory  # generated sync facade
```
and add `"Metaphactory"` to `__all__`.

Run:
```bash
python -c "from metaphactory_automation import Metaphactory; from metaphactory_automation.aio import Metaphactory as A; print('sync+async import OK')"
```
Expected: prints `sync+async import OK`.

- [ ] **Step 6: Run test to verify it passes**

Run: `pytest tests/unit/test_sync_generated.py -v`
Expected: PASS (2 passed)

- [ ] **Step 7: Add a CI guard that generated sync is up to date**

Add to `build_sync.py` a `--check` mode:

```python
# append inside build_sync.py, replacing the `if __name__` block:
import sys

def _check() -> int:
    before = {m: (SYNC_DIR / f"{m}.py").read_text() if (SYNC_DIR / f"{m}.py").exists() else ""
              for m in SYNC_MODULES}
    main()
    drift = [m for m in SYNC_MODULES if (SYNC_DIR / f"{m}.py").read_text() != before[m]]
    if drift:
        print("Sync modules out of date, re-run build_sync.py:", drift)
        return 1
    print("Sync modules up to date.")
    return 0

if __name__ == "__main__":
    sys.exit(_check() if "--check" in sys.argv else (main() or 0))
```

- [ ] **Step 8: Commit (including generated sync files)**

```bash
git add build_sync.py src/metaphactory_automation/*.py src/metaphactory_automation/__init__.py tests/unit/test_sync_generated.py
git commit -m "build(lib): generate sync package from async via unasync"
```

---

### Task 13: Integration tests + docker-compose

**Files:**
- Create: `docker-compose.yml`
- Create: `tests/integration/conftest.py`
- Create: `tests/integration/test_vocabulary_flow.py`
- Create: `tests/integration/test_sparql_flow.py`

- [ ] **Step 1: Write `docker-compose.yml`**

```yaml
# docker-compose.yml — spin up a metaphactory for integration tests
services:
  metaphactory:
    image: metaphacts/metaphactory:5.10.0
    ports:
      - "10214:8080"
    environment:
      PLATFORM_OPTS: "-Dconfig.environment.shiroAuthenticationFilter=anonymous,authc"
    # Provide a license via env or volume if your image requires one:
    # volumes:
    #   - ./metaphactory-license.txt:/runtime-data/config/license.txt:ro
```

- [ ] **Step 2: Write integration conftest (skips when no instance)**

```python
# tests/integration/conftest.py
import os
import pytest

MF_URL = os.environ.get("MF_URL")

def pytest_collection_modifyitems(config, items):
    if MF_URL:
        return
    skip = pytest.mark.skip(reason="set MF_URL to run integration tests")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip)

@pytest.fixture
def mf_config():
    return {
        "url": os.environ["MF_URL"],
        "user": os.environ.get("MF_USER", "admin"),
        "password": os.environ.get("MF_PASS", "admin"),
    }
```

- [ ] **Step 3: Write the SPARQL integration test**

```python
# tests/integration/test_sparql_flow.py
import pytest
from metaphactory_automation.aio import Metaphactory

@pytest.mark.integration
async def test_sparql_insert_and_query_roundtrip(mf_config):
    async with Metaphactory(mf_config["url"], mf_config["user"], mf_config["password"]) as mf:
        await mf.sparql.update(
            "INSERT DATA { GRAPH <urn:test:mfauto> { "
            "<urn:test:a> <urn:test:p> \"hello\" } }"
        )
        result = await mf.sparql.query(
            "SELECT ?o WHERE { GRAPH <urn:test:mfauto> { <urn:test:a> <urn:test:p> ?o } }"
        )
        assert any(row["o"] == "hello" for row in result)
        # cleanup
        await mf.sparql.update("DROP GRAPH <urn:test:mfauto>")
```

- [ ] **Step 4: Write the vocabulary integration test**

```python
# tests/integration/test_vocabulary_flow.py
import pytest
from metaphactory_automation.aio import Metaphactory

@pytest.mark.integration
async def test_create_vocabulary_with_hierarchy(mf_config):
    async with Metaphactory(mf_config["url"], mf_config["user"], mf_config["password"]) as mf:
        voc = await mf.vocabularies.create("IntegrationTest Vegetables")
        await voc.add_top_concept("Vegetables", "All vegetables")
        await voc.add_narrower("Vegetables", "Carrot", "Root vegetable")
        await voc.set_status("Carrot", "In review")
        await voc.commit()
        # Verify via SPARQL that the concept landed.
        result = await mf.sparql.query(
            'SELECT ?l WHERE { ?c a <http://www.w3.org/2004/02/skos/core#Concept> ; '
            '<http://www.w3.org/2004/02/skos/core#prefLabel> ?l . '
            'FILTER(STR(?l) = "Carrot") }'
        )
        assert len(result) >= 1
```

- [ ] **Step 5: Run integration tests against a live instance**

Run:
```bash
docker compose up -d
# wait for metaphactory to be ready (first boot can take ~60-90s)
MF_URL=http://localhost:10214 pytest tests/integration -v -m integration
docker compose down
```
Expected: both integration tests PASS. If the vocabulary test fails on a
selector, update the relevant field in `SelectorProfile` (selectors.py) — that
is the intended maintenance point — and re-run. If SPARQL auth fails over HTTP,
the browser-login path in the client already supplies the cookie; confirm the
`sparql_path` and `update` param names against your version.

- [ ] **Step 6: Commit**

```bash
git add docker-compose.yml tests/integration
git commit -m "test(lib): integration tests for vocabulary + sparql flows"
```

---

### Task 14: CI (GitHub Actions)

**Files:**
- Create: `.github/workflows/lib-ci.yml` (repo root, not under lib/)

- [ ] **Step 1: Write the workflow**

```yaml
# .github/workflows/lib-ci.yml
name: lib-ci
on:
  pull_request:
    paths: ["lib/metaphactory-automation/**", ".github/workflows/lib-ci.yml"]
  push:
    branches: [main]
    paths: ["lib/metaphactory-automation/**"]
  schedule:
    - cron: "0 3 * * *"   # nightly integration
  workflow_dispatch:

defaults:
  run:
    working-directory: lib/metaphactory-automation

jobs:
  lint-type-unit:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ["3.10", "3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - run: python -m pip install -e ".[dev]"
      - run: python build_sync.py --check
      - run: ruff check .
      - run: mypy
      - run: pytest tests/unit -v

  integration:
    if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m pip install -e ".[dev]"
      - run: python -m playwright install --with-deps chromium
      - run: docker compose up -d
      - name: Wait for metaphactory
        run: |
          for i in $(seq 1 60); do
            if curl -sf -o /dev/null http://localhost:10214/login; then echo ready; break; fi
            sleep 5
          done
      - run: MF_URL=http://localhost:10214 pytest tests/integration -v -m integration
      - run: docker compose down
        if: always()
```

- [ ] **Step 2: Validate workflow YAML locally**

Run:
```bash
python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/lib-ci.yml')); print('yaml ok')"
```
Expected: prints `yaml ok` (run from repo root; adjust path).

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/lib-ci.yml
git commit -m "ci(lib): lint+type+unit on PR, integration nightly"
```

---

### Task 15: README, CHANGELOG, docs, and release prep

**Files:**
- Create: `lib/metaphactory-automation/README.md`
- Create: `lib/metaphactory-automation/CHANGELOG.md`
- Create: `lib/metaphactory-automation/mkdocs.yml`
- Create: `lib/metaphactory-automation/docs/index.md`
- Modify: root `README.md` (link to the library)

- [ ] **Step 1: Write the package `README.md`**

```markdown
# metaphactory-automation

> **Unofficial.** Not affiliated with or endorsed by metaphacts GmbH.
> "metaphactory" is a trademark of metaphacts GmbH.

Hybrid HTTP + Playwright automation for the metaphactory platform. SPARQL and
data operations go over HTTP; the visual editors that only exist in the browser
are driven with Playwright — behind one client.

## Install

    pip install metaphactory-automation
    playwright install chromium

## Quickstart (sync)

```python
from metaphactory_automation import Metaphactory

with Metaphactory("http://localhost:10214", "admin", "admin", headless=True) as mf:
    voc = mf.vocabularies.create("Vegetables")
    voc.add_top_concept("Vegetables", "All vegetables")
    voc.add_narrower("Vegetables", "Carrot")
    voc.set_status("Carrot", "In review")
    voc.commit()

    for row in mf.sparql.query("SELECT * WHERE {?s ?p ?o} LIMIT 5"):
        print(row)
```

## Async

```python
from metaphactory_automation.aio import Metaphactory

async with Metaphactory(url, user, pw) as mf:
    rows = await mf.sparql.query("SELECT * WHERE {?s ?p ?o} LIMIT 5")
```

## Version compatibility

Selectors are verified against metaphactory 5.10.0. For other versions, override
the profile:

```python
from dataclasses import replace
from metaphactory_automation.selectors import PROFILE_5_10_0
profile = replace(PROFILE_5_10_0, codemirror=".cm-editor")
Metaphactory(url, user, pw, selector_profile=profile)
```

MIT licensed.
```

- [ ] **Step 2: Write `CHANGELOG.md`**

```markdown
# Changelog

## [0.1.0] - 2026-05-26
### Added
- `Metaphactory` client (sync + async) with shared-cookie HTTP + Playwright transports.
- `mf.vocabularies`: create vocabulary, add top/narrower concepts, set status, commit.
- `mf.sparql`: query and update over HTTP.
- Versioned `SelectorProfile` (5.10.0 default, overridable).
- Typed error hierarchy; functional helpers escape hatch (`mf.helpers`).
```

- [ ] **Step 3: Write minimal mkdocs config and index**

```yaml
# mkdocs.yml
site_name: metaphactory-automation
theme:
  name: material
nav:
  - Home: index.md
```

```markdown
<!-- docs/index.md -->
# metaphactory-automation

Unofficial hybrid HTTP + Playwright automation for metaphactory.
See the README for quickstart. Not affiliated with metaphacts GmbH.
```

- [ ] **Step 4: Link the library from the root README**

Add to the root `README.md` layout table (under the existing rows):

```markdown
| `lib/metaphactory-automation/` | The published Python library (`pip install metaphactory-automation`) |
```

- [ ] **Step 5: Build the wheel and verify metadata**

Run:
```bash
cd lib/metaphactory-automation
python -m pip install build
python -m build
python -m pip install twine && twine check dist/*
```
Expected: builds `metaphactory_automation-0.1.0-py3-none-any.whl` and sdist;
`twine check` reports PASSED.

- [ ] **Step 6: Commit**

```bash
git add lib/metaphactory-automation/README.md lib/metaphactory-automation/CHANGELOG.md lib/metaphactory-automation/mkdocs.yml lib/metaphactory-automation/docs README.md
git commit -m "docs(lib): readme, changelog, mkdocs, root link; v0.1.0 release prep"
```

- [ ] **Step 7 (manual, gated on user): publish to PyPI**

Publishing is a one-way, outward-facing action — do NOT run without explicit
user confirmation. When approved (PyPI account + trusted publishing or token
configured):

```bash
cd lib/metaphactory-automation
twine upload dist/*
git tag lib-v0.1.0
git push origin lib-v0.1.0
```

---

## Self-Review

**Spec coverage:**
- Distribution/naming/trademark → Task 1 (pyproject), Task 15 (README disclaimer). ✓
- Repo layout under `lib/` → all tasks. ✓
- Layer 0 transport (auth/browser/http, shared cookie) → Tasks 5, 6, 7, 11. ✓
- Layer 1 functional helpers (escape hatch) → Task 8, exposed via `mf.helpers` (Task 11). ✓
- Layer 2 OO client (`mf.vocabularies`, `mf.sparql`) → Tasks 9, 10, 11. ✓
- Public API shape → Tasks 11, 15 (README matches). ✓
- Sync+async via unasync → Task 12. ✓
- Selector profile (versioned, overridable) → Task 3, used throughout. ✓
- Error hierarchy → Task 2. ✓
- Testing (unit always; integration opt-in/docker) → Tasks 2–12 (unit), 13 (integration). ✓
- Tooling/CI (ruff, mypy, pytest, GH Actions, mkdocs, changelog) → Tasks 1, 14, 15. ✓
- v0.1.0 scope (vocabularies + sparql only) → Tasks 9, 10; ontologies/templates/AI explicitly excluded. ✓
- Risks (auth fallback, selector drift, unasync drift guard, gated integration) → Tasks 11 (browser-login cookie), 3, 12 (--check), 13/14. ✓

**Placeholder scan:** No TBD/TODO; every code step has complete code; commands have expected output. ✓

**Type consistency:** `SelectorProfile` fields referenced in `helpers.py` match Task 3 definitions; `HttpSession.query/update` (Task 6) match `SparqlAPI` calls (Task 9); `BrowserSession.page/selectors/dismiss_modals/navigate` (Task 7) match usage in `vocabularies.py` (Task 10) and `client.py` (Task 11); `Metaphactory` attrs (`vocabularies`, `sparql`, `helpers`, `page`, `_base_url`, `_selectors`) match unit tests. ✓

**Known execution-time validations (by design, not placeholders):** exact login POST cookie name, `sparql_path`, and UPDATE param are confirmed by the Task 13 integration tests; selector drift is the intended `SelectorProfile` maintenance point.
```
